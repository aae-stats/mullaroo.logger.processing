#-------------------------------------------------------------------------------
# Name:        mullaroo acoustic data prep
# Purpose:     mullaroo acoustic data prep
#
# Author:      7810AK
#
# Created:     24/04/2019
# Copyright:   (c) 7810AK 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import csv
import common
import local_vars
from datetime import *

prevItem = ''
part = None


today = date.today()
date_string = today.strftime('%y%m%d')
filename = 'acoustic_data_' + today.strftime('%Y') + '_'

fo = open(f'{local_vars.acou_outPath}/{filename}{date_string}.csv', 'w')
#write header of output file
fo.write("date_time,receiver,transmitter,transmitter_name,transmitter_serial,sensor_value,sensor_unit,station_name,latitude,longitude,file\n")

fo2 = open(f'{local_vars.acou_outPath}/{filename}counts_{date_string}.csv', 'w')
##############acou_outPath#########################################################################


#Batch read file names
items = common.getFileNames(local_vars.acou_inPath, '.csv')

#get file
for item in items:
    print(item)
    #read in data
    file = open(local_vars.acou_inPath + "/" + item, "rb")
    output = 0

    for line in file:
        if output > 0:
            # print( str(line))
            line = str(line).strip() #line.encode('utf-8').strip().decode( "utf-8" ) # str(line).replace("b'", "")
            line = line.replace("b'", "")
            line = line.replace("\\r\\n'", "")
            part = str(line).split(',')
##            print(part[0])
##            if output * (output + 1) > 0 and part[0] != "":
            if len(part) > 7:
                line = str(line) + ",,," + str(item).replace(".csv", "") + "\n"
            else:
                line = str(line) + ",,,,,,,," + str(item).replace(".csv", "") + "\n"
            fo.write(line)

            if "Stationary targets" in line:
                print("Stationary targets HIT!")
                fo2.write(f'{part[0]},{item}\n')

##            if part[0] == "":
##                if output == 0 and item != prevItem:
##                    output = 1
##                    prevItem = item
##                else:
##                    output = 0

        output = output + 1

##    fo2.write('{0},{1}\n'.format(item, output))
    if part != None:
        fo2.write(f'{part[0]},{item}\n')
##        print(output)
#This file contains 2362 Stationary targets

    file.close()
    prevItem = item

fo.close()
fo2.close()