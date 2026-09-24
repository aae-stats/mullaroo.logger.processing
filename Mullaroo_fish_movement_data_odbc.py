#-------------------------------------------------------------------------------
# Name:        all tracking data filtering
# Purpose:
#
# Author:      ak34
#
# Created:     14/05/2021
# Copyright:   (c) ak34 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##import sys
##import csv
import datetime
import common
##import psycopg2
import local_vars
from psycopg2 import Error

current_time = datetime.datetime.now()

fe = None

# DEAL WITH DUPLICATE TRACKING RECORDS BEFORE RUNNNING!!!!

def getdatetime():
    d = datetime.datetime.now()
    return d.strftime("%Y") + "-" + d.strftime("%m") + "-" + d.strftime("%d")

def get_SQL(prev_record, date_st):
##    print('almost there')
##    if prev_yr is null:
##        prev_yr = -1
##        print(prev_yr)


##  day		         	0
##  month		           	1
##  yr		          	2
##  julian_day	       	3
##  tag_no		      	4
##  species		     	5
##  length		      	6
##  weight		      	7
##  capture_zone_id		8
##  detection_logger  	9
##  zone_id	      		10
##  source	       		11
##  log_type	         	12
##  mull_flow	        	13
##  mull_temp	        	14
##  lock_8_flow	      	15
##  lock_8_us_level		16
##  lock_8_temp	      	17
##  lock_7_flow	      	18
##  lock_7_us_level		19
##  lock_7_us_do  		20
##  lock_7_ds_do  		21
##  rufus_river_do		22
##  tracking_processed_dt 23
##  output_dt		        24




    try:

        sql = "INSERT INTO mullaroo.mullaroo_fish_movement_data (day, month, yr, julian_day, tag_no, species, length, weight, capture_zone_id, detection_logger, zone_id, \
        source, log_type, mull_flow, mull_temp, lock_8_flow, lock_8_us_level, lock_8_temp, lock_7_flow, lock_7_us_level, \
        lock_7_us_do, lock_7_ds_do, rufus_river_do, tracking_processed_dt, output_dt) \
        VALUES ({0},{1},{2},{3},'{4}','{5}',{6},{7},{8},'{9}',{10},'{11}','{12}',{13},{14},{15},{16},{17},{18},{19},{20},{21},{22},'{23}'::date,'{24}'::date) \
        ".format(prev_record[0], prev_record[1], prev_record[2], prev_record[3], prev_record[4], prev_record[5], prev_record[6], prev_record[7], prev_record[8], prev_record[9],
        prev_record[10], prev_record[11], prev_record[12], prev_record[13], prev_record[14], prev_record[15], prev_record[16], prev_record[17], prev_record[18], prev_record[19],
        prev_record[20], prev_record[21], prev_record[22], prev_record[23], date_st)


        return sql

    except (Exception, Error) as error:
        print(error)


try:
    # Connect to an existing database

    # Create a cursor to perform database operations
##    cur = connection.cursor()
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
    outPath = local_vars.data_outPath
    prevItem = ''
    date_string = getdatetime()
    #**********************************************************************************************************

    errorFile = "mullaroo_fish_movement_data_ERROR_" + common.getdatetime() + ".csv"

    #DELETE FROM mullaroo.acoustic_data_filtered
    query = "DELETE FROM mullaroo.mullaroo_fish_movement_data"
    cur.execute(query)
    local_vars.connection.commit()

    query = "ALTER SEQUENCE mullaroo.mullaroo_fish_movement_data_rec_id_seq RESTART WITH 1;"
    cur.execute(query)
    local_vars.connection.commit()


    prev_tag = "-1"
    prev_record = ""
    count = 0
    stop_out = 0

    cur.execute("SELECT day, month, yr, julian_day, tag_no, species, length, weight, capture_zone_id, detection_logger, zone_id, \
    source, log_type, mull_flow, mull_temp, lock_8_flow, lock_8_us_level, lock_8_temp, lock_7_flow, lock_7_us_level, lock_7_us_do, \
    lock_7_ds_do, rufus_river_do, tracking_processed_dt, post_expiry, post_last_rec \
	FROM mullaroo.v_mullaroo_fish_movement_data_raw \
    ORDER BY tag_no, yr, julian_day;")

    #        WHERE tag_no IN ('132.02','132.20a') \

##    errorHeader = "day,month,yr,julian_day,tag_no,species,length,weight,capture_zone_id,detection_logger,zone_id,source,log_type,mull_flow,mull_temp,lock_8_flow,lock_8_us_level,lock_8_temp,lock_7_flow,lock_7_us_level,lock_7_us_do,lock_7_ds_do,rufus_river_do,tracking_processed_dt,post_expiry,post_last_rec\n"
    errorHeader = "tag_no,year,julian_day,detection_logger,source\n"

    records = cur.fetchall()
    rec_total = len(records)

    for record in records:

        if record[4] != prev_tag:
            stop_out = 0
            if prev_tag != "-1":
##                print('got to 1')
                insert_query = get_SQL(prev_record, date_string)
                cur.execute(insert_query.replace('None', 'NULL'))
                local_vars.connection.commit()
                print('{0} of {1}'.format(count, rec_total))

            prev_tag = record[4]
            prev_record = record
##            count = count + 1

        else:

            if prev_record[2] == record[2] and prev_record[3] == record[3]:
                #print out duplicate records
##                outStr = ', '.join(map(" ".join, prev_record))
##                outStr = prev_record.iloc[1,:].to_string(header=False, index=False)
                outStr = '{0},{1},{2},{3},{4}\n'.format(record[4], record[2], record[3], record[9], record[11])
                errorLogged = common.writeError(fe, outPath, errorFile, outStr, errorHeader)

##                outStr = ', '.join(map(" ".join, record))
##                outStr = record.iloc[1,:].to_string(header=False, index=False)
                outStr = '{0},{1},{2},{3},{4}\n'.format(prev_record[4], prev_record[2], prev_record[3], prev_record[9], prev_record[11])
                errorLogged = common.writeError(fe, outPath, errorFile, outStr, errorHeader)
                print('*** Duplicate found: tag {0} - {1}-{2}'.format(record[4], record[2], record[3]))

            if stop_out == 0:
                if record[9] is None: #detection_logger
                    if record[24] == "post_expiry" and record[25] == "post_last_rec":
                        stop_out = 1 #stop outputting records for this tag
                    else:
    ##                print('got to 2')
                        insert_query = get_SQL(prev_record, date_string)
                        cur.execute(insert_query.replace('None', 'NULL'))
                        local_vars.connection.commit()
                        cur_rec = list(record)
                        cur_rec[8] = prev_record[8] #capture_zone_id
                        if cur_rec[24] == 'post_expiry':
                            cur_rec[9] = 'previously expired' #detection_logger
                        else:
                            cur_rec[9] = 0 #detection_logger
                        cur_rec[10] = prev_record[10] #zone_id
                        cur_rec[11] = prev_record[11] #source
                        cur_rec[12] = "inferred" #log_type
                        cur_rec = tuple(cur_rec)
                        prev_record = cur_rec
                else:
    ##                print('got to 3')
                    insert_query = get_SQL(prev_record, date_string)
                    cur.execute(insert_query.replace('None', 'NULL'))
                    local_vars.connection.commit()
                    cur_rec = list(record)
                    if cur_rec[9].lower() == 'expired':
                        cur_rec[10] = prev_record[10]

                    prev_record = cur_rec
                    if prev_record[12] == "removal":
                        stop_out = 1 #stop outputting records for this tag
                    if prev_record[24] != "valid" and prev_record[25] != "valid":
                        stop_out = 1 #stop outputting records for this tag

        count = count + 1
        print('{0} of {1}'.format(count, rec_total))


    insert_query = get_SQL(prev_record, date_string)
    cur.execute(insert_query.replace('None', 'NULL'))
    local_vars.connection.commit()
##    print(line.rstrip())
    print('{0} of {1}'.format(count, rec_total))
    print('Start: {0}'.format(current_time))
    current_time = datetime.datetime.now()
    print('Finish: {0}'.format(current_time))

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:

    if (local_vars.connection):
        cur.close()
        local_vars.connection.close()
        print("PostgreSQL connection is closed")

##    if (connection):
##        cur.close()
##        connection.close()
##        print("PostgreSQL connection is closed")