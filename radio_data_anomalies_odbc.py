#-------------------------------------------------------------------------------
# Name:        radio data identify anomalies
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
##sys.path.insert(0, 'O:/DATA/DOCS/PROJECTS/SNAGS/OTHER_PROJECTS/MULLAROO/radio tower')
import local_vars
##import common
##import psycopg2
from psycopg2 import Error

global connection
global cur

##global sig_max
##global id_max
##global prev_tag_no
##global prev_yr
##global prev_jday
##global prev_min
##global prev_logger_id

sig_max = -1
prev_id = 0
prev_tag_no = ""
prev_yr = 0
prev_jday = -1
prev_min = -1
alive_on_change = 0
count = 1

def updateStatus(_id):
##    print('almost there')
##    if prev_yr is null:
##        prev_yr = -1
##        print(prev_yr)
    try:

        if prev_yr > 0:
##            print('did it')
                        sql = "UPDATE mullaroo.radio_data_new SET status = 'anomaly2' WHERE id = {0}".format(_id)
##                        sql = "UPDATE mullaroo.radio_data_new_wkshp SET status = 'anomaly2' WHERE id = {0}".format(_id)
                        cur.execute(sql)
                        local_vars.connection.commit()

    except (Exception, Error) as error:
        print(error)

try:
    # Connect to an existing database
    # Create a cursor to perform database operations
    cur = local_vars.connection.cursor()
    # Print PostgreSQL details
    # Executing a SQL query\
    cur.execute("SELECT version();")
    # Fetch result
    record = cur.fetchone()
    print('you are connected to - {0}'.format(record))



# tag_no, logger_number, dt, yr, jday, min_rank, rec_count
# WHERE tag_no LIKE '51257'
    cur.execute("SELECT id, tag_no, year, jday, hour, min, ant, sig_strength, count, logger_id, zone_id, strongest_sig, status, orig_ant \
                 FROM mullaroo.radio_data_new \
                 WHERE status LIKE 'alive' AND ant > 0 \
                 ORDER BY tag_no, year, jday, hour, min;")

##    cur.execute("SELECT id, tag_no, year, jday, hour, min, ant, sig_strength, count, logger_id, zone_id, strongest_sig, status, orig_ant \
##                   FROM mullaroo.radio_data_new_wkshp \
##                   WHERE status LIKE 'alive' AND ant > 0 \
##                   ORDER BY tag_no, year, jday, hour, min;")

    records = cur.fetchall()

    for record in records:

##        print (record)
        id = record[0]
        tag_no = record[1]
        yr = record[2]
        jday = record[3]
##        print(('record {0}, ID: {1} tag: {2}').format(count, id, tag_no))

##        print(prev_yr)

        if tag_no == prev_tag_no:

            if yr == prev_yr:

                if jday == prev_jday or (jday - prev_jday) == 1:

                    #this is a good record
                    alive_on_change = 1
                    prev_jday = jday
                    prev_id = id
                    prev_tag_no = tag_no
                    prev_yr = yr

                else:

                    if alive_on_change == 0:
                        updateStatus(prev_id)
                        print(prev_id)

                    prev_jday = jday
                    prev_id = id
                    prev_tag_no = tag_no
                    prev_yr = yr
                    alive_on_change = 0

            else:

                    if alive_on_change == 0:
                        updateStatus(prev_id)
                        print(prev_id)

                    prev_jday = jday
                    prev_id = id
                    prev_tag_no = tag_no
                    prev_yr = yr
                    alive_on_change = 0


        else:
                    if alive_on_change == 0:
                        updateStatus(prev_id)
                        print(prev_id)

                    prev_jday = jday
                    prev_id = id
                    prev_tag_no = tag_no
                    prev_yr = yr
                    alive_on_change = 0

##'            prev_tag_no = tag_no
        count = 1 + count


except (Exception, Error) as error:
    print("*** Error while connecting to DB", error)
finally:
##    fo.close()

    if (local_vars.connection):
        cur.close()
        local_vars.connection.close()
        print("DB connection is closed")
