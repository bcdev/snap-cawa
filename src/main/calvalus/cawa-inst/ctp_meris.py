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
        months  = [ '07' ]
        #months  = [ '06' ]
        #months  = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12' ]

    return months

def getMinMaxDate(year, month):
    monthrange = calendar.monthrange(int(year), int(month))
    minDate = datetime.date(int(year), int(month), 1)
    maxDate = datetime.date(int(year), int(month), monthrange[1])
    return (minDate, maxDate)

####################################################################

#### main script: ####

#years   = [ '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011','2012' ]
years   = [ '2005' ]

inputs = []
for year in years:
    for month in getMonths(year):
        #inputs.append('/calvalus/projects/cawa/idepix_ctp/meris/' + year + '/' + month)
        inputs.append('/calvalus/projects/cawa/idepix_ctp/meris-nc/' + year + '/' + month)

hosts  = [('localhost',16)]
types  = [('ctp-step.sh',4), ('ctp-format-step.sh',2)]

pm = PMonitor(inputs, \
              request='ctp_meris', \
              logdir='log', \
              hosts=hosts, \
              types=types)

for year in years:
    for month in getMonths(year):
        (minDate, maxDate) = getMinMaxDate(year, month)
        #(minDate, maxDate) = ('2005-07-01', '2005-07-02')
        pm.execute('ctp-step.sh', \
                   [ '/calvalus/projects/cawa/idepix_ctp/meris-nc/' + year + '/' + month ], \
                   [ '/calvalus/projects/cawa/ctp/meris/' + year + '/' + month ], \
                   parameters=['MERIS', str(minDate), str(maxDate)])  
        pm.execute('ctp-format-step.sh', \
                   [ '/calvalus/projects/cawa/ctp/meris/' + year + '/' + month ], \
                   [ '/calvalus/projects/cawa/ctp/meris-nc/' + year + '/' + month ], \
                   parameters=['MERIS', str(minDate), str(maxDate)])

pm.wait_for_completion()
