import glob
import os
import datetime
from datetime import timedelta
import calendar
from pmonitor import PMonitor

####################################################################

def getMinMaxDate(year, month):
    monthrange = calendar.monthrange(int(year), int(month))
    minDate = datetime.date(int(year), int(month), 1)
    maxDate = datetime.date(int(year), int(month), monthrange[1])
    return (minDate, maxDate)

####################################################################

#### main script: ####

years   = [ '2008' ]

base_date = datetime.date(2008,1,1)

inputs = []
for year in years:
    for day in range(1,122): # 20080101 - 20080430
    #for day in range(1,32): # Jan, TODO: many broken products, repeat download of MYD021KM for Jan
    #for day in range(2,3):
    #for day in range(1,58): # Jan, Feb
    #for day in range(58,122): # Mar, Apr
        doy = str(day).zfill(3)
        inputs.append('/calvalus/projects/cawa/MODIS_MYD021KM/' + year + '/' + doy)

hosts  = [('localhost',16)]
types  = [('idepix-step.sh',16), 
          ('era-interim-modis-step.sh',4),
          ('idepix-format-step.sh',2)]

pm = PMonitor(inputs, \
              request='idepix_modis', \
              logdir='log', \
              hosts=hosts, \
              types=types)

for year in years:
    for day in range(1,122): # 20080101 - 20080430
    #for day in range(1,32): # Jan, TODO: many broken products, repeat download of MYD021KM for Jan
    #for day in range(2,3):
    #for day in range(1,58): # Jan, Feb
    #for day in range(58,122): # Mar, Apr
        doy = str(day).zfill(3)
        current_date = base_date + timedelta(day-1)
        datestring = current_date.strftime("%Y-%m-%d")
        pm.execute('era-interim-modis-step.sh', \
                   [ '/calvalus/projects/cawa/MODIS_MYD021KM/' + year + '/' + doy ], \
                   [ '/calvalus/projects/cawa/era-interim/modis/' + year + '/' + doy ], \
                   parameters=['MODIS', datestring, datestring])
        pm.execute('idepix-step.sh', \
                   [ '/calvalus/projects/cawa/MODIS_MYD021KM/' + year + '/' + doy ,
                     '/calvalus/projects/cawa/era-interim/modis/' + year + '/' + doy], \
                   [ '/calvalus/projects/cawa/idepix/modis/' + year + '/' + doy ], \
                   parameters=['MODIS', datestring, datestring])  
        pm.execute('idepix-format-step.sh', \
                   [ '/calvalus/projects/cawa/idepix/modis/' + year + '/' + doy ], \
                   [ '/calvalus/projects/cawa/idepix/modis-nc/' + year + '/' + doy ], \
                   parameters=['MODIS', datestring, datestring])

pm.wait_for_completion()
