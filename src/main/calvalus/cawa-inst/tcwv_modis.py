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
months  = [ '01', '02', '03', '04' ]

#days = [2, 20]
days = [90, 120]

base_date = datetime.date(2008,1,1)

inputs = []
for year in years:
    #for day in range(122): # 20080101 - 20080430
    #for day in range(15,17): # 20080115, 20080116
    #for day in range(1,58): # Jan, Feb
    for day in days:
        doy = str(day).zfill(3)
        #inputs.append('/calvalus/projects/cawa/idepix/modis-nc/' + year + '/' + doy)
        inputs.append('/calvalus/projects/cawa/idepix/modis/' + year + '/' + doy)

hosts  = [('localhost',16)]
types  = [('tcwv-step.sh',4), ('tcwv-format-step.sh',2)]

pm = PMonitor(inputs, \
              request='tcwv_modis', \
              logdir='log', \
              hosts=hosts, \
              types=types)

for year in years:
    #for day in range(122): # 20080101 - 20080430
    #for day in range(15,17): # 20080115, 20080116
    #for day in range(1,58): # Jan, Feb
    for day in days:
        doy = str(day).zfill(3)
        current_date = base_date + timedelta(day-1)
        datestring = current_date.strftime("%Y-%m-%d")
        pm.execute('tcwv-step.sh', \
                   [ '/calvalus/projects/cawa/idepix/modis/' + year + '/' + doy ], \
                   [ '/calvalus/projects/cawa/tcwv/modis/' + year + '/' + doy ], \
                   parameters=['MODIS', datestring, datestring])  
        pm.execute('tcwv-format-step.sh', \
                   [ '/calvalus/projects/cawa/tcwv/modis/' + year + '/' + doy ], \
                   [ '/calvalus/projects/cawa/tcwv/modis-nc/' + year + '/' + doy ], \
                   parameters=['MODIS', datestring, datestring])

pm.wait_for_completion()
