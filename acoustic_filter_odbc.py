#-------------------------------------------------------------------------------
# Name:        acoustic data filtering
# Purpose:
#
# Author:      ak34
#
# Created:     07/05/2021
# Copyright:   (c) ak34 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##import sys
##import csv
import common
import local_vars
##import psycopg2
from psycopg2 import Error

try:
    # Connect to an existing database
    # Create a cursor to perform database operations
    cur = local_vars.connection.cursor()
    # Print PostgreSQL details
##    print("PostgreSQL server information")
##    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query\
    cur.execute("SELECT version();")
    # Fetch result
    record = cur.fetchone()
    print("You are connected to - ", record, "\n")

    #**********************************************************************************************************
    outPath = local_vars.acou_filt_outPath
    prevItem = ''
    date_string = common.getdate()
    filename = 'acoustic_filtered_'
    #**********************************************************************************************************



    #DELETE FROM mullaroo.acoustic_data_filtered
    delete_query = "DELETE FROM mullaroo.acoustic_data_filtered2"
    cur.execute(delete_query)
    local_vars.connection.commit()


    fo = open(outPath + "/" + filename + date_string  + ".csv", 'w')
    #write header of output file
    fo.write("tag_no,logger_number,yr,jday\n")


    prev_tag = "-1"
    prev_yr = "-1"
    prev_jday = "-1"
    prev_logger = 0
    prevday_logger = 0
    max_val = 0
    count = 1

# tag_no, logger_number, dt, yr, jday, min_rank, rec_count
# WHERE tag_no LIKE '51257'
    cur.execute("SELECT tag_no, logger_number, yr, jday, min_rank, rec_count \
    FROM mullaroo.v_acoustic_data_all \
##    WHERE tag_no LIKE '21743' \
    ORDER BY tag_no, yr, jday, rec_count DESC;")

    records = cur.fetchall()

    for record in records:

        if record[0] != prev_tag:

            if prev_tag != "-1":
                line = '{0},{1},{2},{3}\n'.format(prev_tag, prev_logger, prev_yr, prev_jday)
                fo.write(line)
                insert_query = "INSERT INTO mullaroo.acoustic_data_filtered2 (tag_no,logger_number,yr,jday) VALUES ({0},{1},{2},{3})".format(prev_tag, prev_logger, prev_yr, prev_jday)
                cur.execute(insert_query)
                local_vars.connection.commit()
                print(line.rstrip())
                count = count + 1
            prev_tag = record[0] # tag_no
            prev_logger = record[1] # logger_number
            prev_yr = record[2] # yr
            prev_jday = record[3] # jday
            max_val = record[5] # rec_count
            prevday_logger = record[1]

        else:
            if prev_yr == record[2] and prev_jday == record[3]:
                if max_val < record[5]: # rec count is smaller than prev same day rec
                    prev_tag = record[0]
                    prev_logger = record[1]
                    prev_yr = record[2]
                    prev_jday = record[3]
                    max_val = record[5]
                elif max_val == record[5]: # rec count is equal to prev same day rec
                    if prevday_logger == record[1]: # take the logger that is the same as the previous day
                        prev_tag = record[0]
                        prev_logger = record[1]
                        prev_yr = record[2]
                        prev_jday = record[3]
                        max_val = record[5]
                    else:
                        print('record skipped')
                        print(record)
                else:
                    print('record skipped')
                    print(record)

            else:
                line = '{0},{1},{2},{3},{4}\n'.format(prev_tag, prev_logger, prev_yr, prev_jday, max_val)
                fo.write(line)
                insert_query = "INSERT INTO mullaroo.acoustic_data_filtered2 (tag_no,logger_number,yr,jday) VALUES ({0},{1},{2},{3})".format(prev_tag, prev_logger, prev_yr, prev_jday)
                cur.execute(insert_query)
                local_vars.connection.commit()
                print(line.rstrip())
                prevday_logger = prev_logger
                count = count + 1
                prev_tag = record[0]
                prev_logger = record[1]
                prev_yr = record[2]
                prev_jday = record[3]
                max_val = record[5]

    line = '{0},{1},{2},{3}\n'.format(prev_tag, prev_logger, prev_yr, prev_jday)
    fo.write(line)
    insert_query = "INSERT INTO mullaroo.acoustic_data_filtered2 (tag_no,logger_number,yr,jday) VALUES ({0},{1},{2},{3})".format(prev_tag, prev_logger, prev_yr, prev_jday)
    cur.execute(insert_query)
    local_vars.connection.commit()
    print(line.rstrip())
    count = count + 1

    print('{0} records'.format(count))

except (Exception, Error) as error:
    print("Error while connecting to DB", error)
finally:
    fo.close()

    if (local_vars.connection):
        cur.close()
        local_vars.connection.close()
        print("DB connection is closed")