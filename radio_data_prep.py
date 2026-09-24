#-------------------------------------------------------------------------------
# Name:        mullaroo radio data prep
# Purpose:     mullaroo radio data prep
#
# Author:      7810AK
#
# Created:     24/04/2019
# Copyright:   (c) 7810AK 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
##import sys
##import csv
import common
import local_vars
import functions as func
from datetime import *

today = date.today()
date_string = today.strftime('%y%m%d')
filename = 'radio_tower_data_' + today.strftime('%Y')

fo = open(f'{local_vars.radio_outPath}/{filename}_{date_string}.csv', 'w')
fo2 = open(f'{local_vars.radio_outPath}/{filename}_counts_{date_string}.csv', 'w')
fo3 = open(f'{local_vars.radio_outPath}/{filename}_headers_{date_string}.csv', 'w')

#write header of output file
fo.write("year,jday,hour,min,ant,freq,code,sig_strength,count,dtype,data_value,mort,file\n")

#######################################################################################

# Target Data File:
# YY-Year,DDD-Day,HH-Hour,MM-Minute,A-Antenna,(FF)FFFF-Frequency,nn-Tag number,TTT-Signal Strength,ddd-Duplicate Count,t-Data Type,mmmm-Data Value(ms),MMM-Mortality Count
# year,jday,hour,min,ant,freq,code,sig_strength,count,dtype,data_value,mort

# Advanced Telemetry Systems' R4500C Series Receiver-Data Logger
# Yr,Day,Hr,Mn,Ant,Fr,Sig,Code,NumDet,NumMort,DataInd,Data,

#######################################################################################

#Batch read file names
items = common.getFileNames(local_vars.radio_inPath, '.csv')

#get file
for item in items:
    print(item)
    #read in data
    file = open(f'{local_vars.radio_inPath}/{item}', "rb")

    line_count = 0
    header_type = ''
    logs = []

    for line in file:

        line = line.strip().decode( "utf-8" ) # str(line).replace("b'", "")
        part = str(line).split(',')

        if part[0].isnumeric():
            if header_type == 'v1':
                logs.append(func.radio_log(part[0],part[1],part[2],part[3],part[4],part[5],part[6],part[7],part[8],part[9],part[10],part[11]))
            elif header_type == 'v2':
                #0,1,2,3,4,5,7,6,8,11,9,10
                logs.append(func.radio_log(part[0],part[1],part[2],part[3],part[4],part[5],part[7],part[6],part[8],part[11],part[9],part[10]))

            line_count += 1

        if line_count == 0:
            fo3.write(str(item).replace(".csv", "") + ',' + line+ "\n")

            # detecting key words in first line
            if 'Target Data File:' in line:
                header_type = 'v1'
            elif "Advanced Telemetry Systems' R4500C Series Receiver-Data Logger" in line:
                header_type = 'v2'
            elif header_type == '':
                print(f'*** HEADER NOT DETECTED ***\n{line}')


        if "Stationary targets" in line:
            fo2.write(f'{part[0]},{item}\n')


    for log in logs:
        line = func.build_out_line_radio(log) + ',' + str(item).replace(".csv", "") + "\n"
        fo.write(line)


    print(f'*** {line_count} lines processed')

    file.close()

#export data to file
fo.close()
fo2.close()
fo3.close()




