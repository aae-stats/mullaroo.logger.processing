#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      7810AK
#
# Created:     13/07/2018
# Copyright:   (c) 7810AK 2018
# Licence:     <your licence>
# Python 3.7
#-------------------------------------------------------------------------------


##import csv
import datetime
import local_vars
from dateutil.relativedelta import relativedelta
##import psycopg2
from psycopg2 import Error


def getdatetime():
    d = datetime.datetime.now()
    return d.strftime("%y") + d.strftime("%m") + d.strftime("%d") + "_" + d.strftime("%H") + d.strftime("%M")

def GetDateFromJulianDay(year, jDay):

    if(year is not None and jDay is not None):
        startDate = datetime.datetime(int(year), 1, 1)

        return startDate + datetime.timedelta(days=(int(jDay) - 1))
    else:
        return datetime.datetime(1900, 1, 1)

def get_SQL(inList):
    try:

        sql = "INSERT INTO mullaroo.tributary_moves (tag_no,species,from_zone,from_location,to_zone,to_location,year,jday,tag_year,tag_jday,date)        VALUES ('{0}','{1}',{2},'{3}',{4},'{5}',{6},{7},{8},{9},'{10}'::date)".format(inList[0], inList[1], inList[2], inList[3], inList[4], inList[5], inList[6], inList[7], inList[8], inList[9],inList[10])

        return sql

    except (Exception, Error) as error:
        print(error)



locations = ['blank','Murray','Mullaroo_Upper','Little_Mullaroo','Mullaroo_Lower','Lindsay_Mid','Lindsay_Upper','Lindsay_Lower','Murray','Murray','Murray','Murray','Potterwalkagee']

print (locations[0])
print (locations[1])
print (locations[12])

##locations[1] = 'Murray'
##locations[2] = 'Mullaroo_Upper'
##locations[3] = 'Little_Mullaroo'
##locations[4] = 'Mullaroo_Lower'
##locations[5] = 'Lindsay_Mid'
##locations[6] = 'Lindsay_Upper'
##locations[7] = 'Lindsay_Lower'
##locations[8] = 'Murray'
##locations[9] = 'Murray'
##locations[10] = 'Murray'
##locations[11] = 'Murray'
##locations[12] = 'Potterwalkagee'

##focus_zones = 'Murray,Mullaroo_Upper,Lindsay_Lower,Lindsay_Upper,Potterwalkagee'

start = datetime.datetime.now()
print ("Started at {0}".format(start))
print ("------- Loading Data -------------")


base_path = local_vars.base_path

#^^^^^^^^^^^^^^^^^^ INPUT FILE FOR VALUE CORRECTIONS ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
##file = open(base_path + "MULLAROO_FISH_MOVEMENT_DATA_190510_missing_mullaroo_temps.csv", "r")

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


prev_tag_no = -1
location = -1

##rec_id,day,month,yr,julian_day,tag_no,species,length,weight,capture_zone_id,detection_logger,zone_id,source,log_type,mull_flow,mull_temp,lock_8_flow,lock_8_us_level,lock_8_temp,lock_7_flow,lock_7_us_level,lock_7_us_do,lock_7_ds_do,rufus_river_do,tracking_processed_dt,output_dt

try:

    #DELETE FROM mullaroo.acoustic_data_filtered
    query = "DELETE FROM mullaroo.tributary_moves"
    cur.execute(query)
    local_vars.connection.commit()

    query = "ALTER SEQUENCE mullaroo.tributary_moves_id_seq RESTART WITH 1;"
    cur.execute(query)
    local_vars.connection.commit()


    prev_tag = "-1"
##    prev_record = ""
    count = 0
    stop_out = 0

##    cur.execute("SELECT rec_id, day, month, yr, julian_day, tag_no, species, length, weight, capture_zone_id, detection_logger, zone_id, source, \
##                log_type, mull_flow, mull_temp, lock_8_flow, lock_8_us_level, lock_8_temp, lock_7_flow, lock_7_us_level, lock_7_us_do, lock_7_ds_do, \
##                rufus_river_do, tracking_processed_dt, output_dt FROM mullaroo.mullaroo_fish_movement_data ORDER BY tag_no, yr, julian_day;")

    cur.execute("SELECT rec_id, day, month, yr, julian_day, tag_no, species, length_mm, weight_g, capture_zone_id, detection_logger, zone_id \
                FROM mullaroo.v_raw_tracking_data ORDER BY tag_no, rec_id;")


##    errorHeader = "tag_no,year,julian_day,detection_logger,source\n"

    records = cur.fetchall()
##    rec_total = len(records)

##    for record in records:


##    header = 0
    for line in records:
##        if header > 0:

        tag_no = line[5].strip()
        species = line[6].strip()
        year = line[3]
        jday = line[4]
        location = line[11]
        date = GetDateFromJulianDay(year, jday)


        if tag_no != prev_tag_no:
            tag_year = line[3]
            tag_jday = line[4]
            from_location = line[11]
            location = -1
            prev_tag_no = tag_no
            print( tag_no)

        else:
            if location != from_location:

                if location <= 12 and from_location <= 12:
                    focus_zones = 'Mullaroo_Upper,Lindsay_Lower,Lindsay_Upper,Potterwalkagee'
                    out_murray = 0
                    out_trib = 0
                    in_murray = 0
                    in_trib = 0



                    if 'Murray'.find(locations[location]) >= 0: out_murray = 1
                    if focus_zones.find(locations[location]) >= 0: out_trib = 1
                    if 'Murray'.find(locations[from_location]) >= 0: in_murray = 1
                    if focus_zones.find(locations[from_location]) >= 0: in_trib = 1

                    #write output
                    if (out_murray == 1 and in_trib == 1) or (in_murray == 1 and out_trib == 1):
##                        print("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}".format(tag_no,species,str(from_location),'from_' + locations[from_location],str(location) ,'to_' + locations[location],year ,jday,tag_year ,tag_jday,str(date)))
                        record =[tag_no,species,str(from_location),'from_' + locations[from_location],str(location) ,'to_' + locations[location],year ,jday,tag_year ,tag_jday,str(date)]
                        ##                                                fo.write(tag_no + ',' + species + ',' + str(from_location) + ',from_' + locations[from_location] + ',' + str(location) + ',to_' + locations[location] + ',' + year  + ',' + jday + ',' + tag_year  + ',' + tag_jday + ',' + str(date) + "\n")          #site_id,veg_id,stream_prop
##                      ',' + year
##                        fo.flush()
##                    print(record)
                        insert_query = get_SQL(record)
##                        print(insert_query)
                        if insert_query is not None:
                            cur.execute(insert_query.replace('None', 'NULL'))
                            local_vars.connection.commit()

                from_location = location


    print('*** Finished pre-processing')
#=========================================================================================================================================
#=========================================================================================================================================
#=========================================================================================================================================
#=========================================================================================================================================

##
##    cur.execute("SELECT id, tag_no, species, from_zone, from_location, to_zone, to_location, year, jday, tag_year, tag_jday, date FROM mullaroo.tibutary_moves ORDER BY tag_no,year, jday;")
##
####    errorHeader = "tag_no,year,julian_day,detection_logger,source\n"
##
##    records = cur.fetchall()
##
##    for line in records:



finally:
##    if fo is not None:
##       fo.close()

    if (local_vars.connection):
        cur.close()
        local_vars.connection.close()
        print("DB connection is closed")

finished = datetime.datetime.now()
diff = relativedelta(finished, start)

print ("Finished {0}".format(finished))
print ("Finished in {0} days {1} hours {2} minutes".format(diff.days, diff.hours, diff.minutes ))

print ("-------------------------------------")