import glob
import os
import datetime
import calendar
from pmonitor import PMonitor

####################################################################

def getMonths(year):
    if year == '2002':
        months  = [ '04', '05', '06', '07', '08', '09', '10', '11', '12' ]
    elif year == '2012':
        months  = [ '01', '02', '03', '04' ]
    else:
        #months  = [ '01' ]
        #months  = [ '02' ]
        #months  = [ '05' ]
        #months  = [ '10', '11' ]
        months  = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]

    return months

def getMinMaxDate(year, month):
    monthrange = calendar.monthrange(int(year), int(month))
    minDate = datetime.date(int(year), int(month), 1)
    maxDate = datetime.date(int(year), int(month), monthrange[1])
    return (minDate, maxDate)

####################################################################

#### main script: ####

#years   = [ '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011','2012' ]
#years   = [ '2006' ]
#years   = [ '2006', '2005', '2004' ]
#years   = [ '2007', '2008', '2009' ]
#years   = [ '2010', '2011', '2012' ]
years   = [ '2002', '2003' ]
#years   = [ '2005', '2006', '2007', '2008', '2009', '2010', '2011','2012' ]

inputs = []
for year in years:
    for month in getMonths(year):
        inputs.append('/calvalus/eodata/MER_RR__1P/r03/' + year + '/' + month)

hosts  = [('localhost',16)]
types  = [('idepix_v10-step.sh',16), 
          ('era-interim-meris-step.sh',4),
          ('idepix-format-step.sh',2)]

pm = PMonitor(inputs, \
              request='idepix_meris_v10', \
              logdir='log', \
              hosts=hosts, \
              types=types)

for year in years:
    for month in getMonths(year):
        (minDate, maxDate) = getMinMaxDate(year, month)
        pm.execute('era-interim-meris-step.sh', \
                   [ '/calvalus/eodata/MER_RR__1P/r03/' + year + '/' + month ], \
                   [ '/calvalus/projects/cawa/era-interim/meris/' + year + '/' + month ], \
                   parameters=['MERIS', str(minDate), str(maxDate)])
        pm.execute('idepix_v10-step.sh', \
                   [ '/calvalus/eodata/MER_RR__1P/r03/' + year + '/' + month ,
                     '/calvalus/projects/cawa/era-interim/meris/' + year + '/' + month], \
                   [ '/calvalus/projects/cawa/idepix/meris/' + year + '/' + month ], \
                   parameters=['MERIS', str(minDate), str(maxDate)])  
        pm.execute('idepix-format-step.sh', \
                   [ '/calvalus/projects/cawa/idepix/meris/' + year + '/' + month ], \
                   [ '/calvalus/projects/cawa/idepix/meris-nc/' + year + '/' + month ], \
                   parameters=['MERIS', str(minDate), str(maxDate)])

pm.wait_for_completion()
