#-------------------------------------------------------------------------------
# Name:        classes and functions
# Purpose:
#
# Author:      ak34
#
# Created:     10/09/2024
# Copyright:   (c) ak34 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#year,jday,hour,min,ant,freq,code,sig_strength,count,dtype,data_value,mort

class radio_log:
    def __init__(self, year, jday, hour, min, ant, freq, code, sig_strength, count, dtype, data_value, mort):
        self.year = year
        self.jday = jday
        self.hour = hour
        self.min = min
        self.ant = ant
        self.freq = freq
        self.code = code
        self.sig_strength = sig_strength
        self.count = count
        self.dtype = dtype
        self.data_value = data_value
        self.mort = mort


def build_out_line_radio(log):
    return f'{log.year},{log.jday},{log.hour},{log.min},{log.ant},{log.freq},{log.code},{log.sig_strength},{log.count},{log.dtype},{log.data_value},{log.mort}'