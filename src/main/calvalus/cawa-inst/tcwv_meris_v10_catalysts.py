import glob
import os
import datetime
import calendar
from pmonitor import PMonitor

####################################################################

def getMonths(year):
    if year == '2004':
        months  = [ '12' ]
    else:
        months  = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]

    return months

def getMinMaxDate(year, month):
    monthrange = calendar.monthrange(int(year), int(month))
    minDate = datetime.date(int(year), int(month), 1)
    maxDate = datetime.date(int(year), int(month), monthrange[1])
    return (minDate, maxDate)

####################################################################

#### main script: ####

#years   = [ '2005','2006' ]
years   = [ '2004' ]

inputs = []
for year in years:
    for month in getMonths(year):
        inputs.append('/calvalus/projects/cawa/idepix/meris-nc/' + year + '/' + month)

hosts  = [('localhost',16)]
types  = [('tcwv_v10-step.sh',4), ('tcwv-format-step.sh',2)]

pm = PMonitor(inputs, \
              request='tcwv_meris_v10_catalysts', \
              logdir='log', \
              hosts=hosts, \
              types=types)

for year in years:
    for month in getMonths(year):
        (minDate, maxDate) = getMinMaxDate(year, month)
        pm.execute('tcwv_v10-step.sh', \
                   [ '/calvalus/projects/cawa/idepix/meris-nc/' + year + '/' + month ], \
                   [ '/calvalus/projects/cawa/tcwv/meris/' + year + '/' + month ], \
                   parameters=['MERIS', str(minDate), str(maxDate)])  
        pm.execute('tcwv-format-step.sh', \
                   [ '/calvalus/projects/cawa/tcwv/meris/' + year + '/' + month ], \
                   [ '/calvalus/projects/cawa/tcwv/meris-nc/' + year + '/' + month ], \
                   parameters=['MERIS', str(minDate), str(maxDate)])

pm.wait_for_completion()
