#-------------------------------------------------------------------------------
# Name:        radio data sig strength sorting
# Purpose:
#
# Author:      ak34
#
# Created:     11/05/2021
# Copyright:   (c) ak34 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##import sys
##import csv
import local_vars
##import common
##import psycopg2
from psycopg2 import Error

global connection
global cur


sig_max = -1
id_max = 0
prev_tag_no = ""
prev_yr = 0
prev_jday = -1
prev_min = -1
prev_logger_id = -1
count = 1


def updateRadioGroup(_ant, _sig_strength, _id, _tag_no, _yr, _jday, _min, _logger_id):
##    print('almost there')
##    if prev_yr is null:
##        prev_yr = -1
##        print(prev_yr)
    try:

        global sig_max
        global id_max
        global prev_tag_no
        global prev_yr
        global prev_jday
        global prev_min
        global prev_logger_id


##        print(prev_yr)

        if prev_yr > 0:
##            print('did it')
            sql = 'UPDATE mullaroo.radio_data_new SET strongest_sig = 1 WHERE id = {0}'.format(id_max)
##            sql = 'UPDATE mullaroo.radio_data_new_wkshp SET strongest_sig = 1 WHERE id = {0}'.format(id_max)
            cur.execute(sql)
            local_vars.connection.commit()
##            _ant, _sig_strength, _id, _tag_no, _yr, _jday, _min, _logger_id
##            line = '{0},{1},{2},{3},{4},{5}'.format(_tag_no, _yr, _jday) # + str(item).replace(".csv", "") + "\n"
##            fo.write(line)


        prev_tag_no = _tag_no
        prev_yr = _yr
        prev_jday = _jday
        prev_min = _min
        prev_logger_id = _logger_id

        id_max = 0
        sig_max = -1

        if _ant > 0:
            id_max = _id
            sig_max = _sig_strength



    except (Exception, Error) as error:
        print(error)



try:
    # Connect to an existing database
##    connection = psycopg2.connect(user="postgres",
##                                  password="aquatic",
##                                  host="localhost",
##                                  port="5435",
##                                  database="ARI_MISC")

##    connection = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=O:\DATA\DOCS\PROJECTS\SNAGS\OTHER_PROJECTS\MULLAROO\DATABASES\Mullaroo_2021_radio_env_data.accdb;')
##    connection = pyodbc.connect('DSN=Mullaroo_Radio_2021;UID="";PWD=""')
    # Create a cursor to perform database operations
    cur = local_vars.connection.cursor()
    # Print PostgreSQL details
##    print("PostgreSQL server information")
##    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query\
    cur.execute("SELECT version();")
    # Fetch result
    record = cur.fetchone()
    print('you are connected to - {0}'.format(record))



# tag_no, logger_number, dt, yr, jday, min_rank, rec_count
# WHERE tag_no LIKE '51257'
    cur.execute("SELECT id, tag_no, year, jday, hour, min, (hour*60)+min AS tmin, logger_id, ant, sig_strength, strongest_sig, \
             zone_id, mort, status FROM mullaroo.radio_data_new \
             WHERE ant > 0 AND status LIKE 'alive' \
             ORDER BY tag_no, year, jday, hour, min, logger_id, ant;")

##    cur.execute("SELECT id, tag_no, year, jday, hour, min, (hour*60)+min AS tmin, logger_id, ant, sig_strength, strongest_sig, \
##             zone_id, mort, status FROM mullaroo.radio_data_new_wkshp \
##             WHERE ant > 0 AND status LIKE 'alive' \
##             ORDER BY tag_no, year, jday, hour, min, logger_id, ant;")

##    cur.execute("SELECT id, tag_no, year, jday, hour, min, (hour*60)+min AS tmin, logger_id, ant, sig_strength, strongest_sig, \
##             zone_id, mort, status FROM mullaroo.radio_data_new \
##             WHERE status LIKE 'alive' AND tag_no like '153.46' AND ant > 0 \
##             ORDER BY tag_no, year, jday, hour, min, logger_id, ant;")

    records = cur.fetchall()

    for record in records:

##        print (record)
        id = record[0]
        tag_no = record[1]
        yr = record[2]
        jday = record[3]
        min = record[6]
        logger_id = record[7]
        ant = record[8]
        sig = record[9]
        print(('record {0}, ID: {1}').format(count, id))

##        print(prev_yr)

        if tag_no == prev_tag_no:

            if yr == prev_yr:

                if jday == prev_jday:

                    if ant == 0 or min - prev_min > 2: #new group
                        updateRadioGroup(ant, sig, id, tag_no, yr, jday, min, logger_id)

                    else:
                        if sig > sig_max:
                            id_max = id
                            sig_max = sig

                    prev_min = min

                else:

#                    prev_jday = jday
                    updateRadioGroup(ant, sig, id, tag_no, yr, jday, min, logger_id)

            else:

##'                prev_yr = yr
                updateRadioGroup( ant, sig, id, tag_no, yr, jday, min, logger_id)

        else:
##            print('prev_yr: {0}'.format(prev_yr))
            updateRadioGroup( ant, sig, id, tag_no, yr, jday, min, logger_id)
##'            prev_tag_no = tag_no
        count = 1 + count

    print("Finished Processing")

except (Exception, Error) as error:
    print("*** Error while connecting to DB", error)
finally:
##    fo.close()

    if (local_vars.connection):
        cur.close()
        local_vars.connection.close()
        print("DB connection is closed")

##    if (connection):
##        cur.close()
##        connection.close()
##        print("PostgreSQL connection is closed")

