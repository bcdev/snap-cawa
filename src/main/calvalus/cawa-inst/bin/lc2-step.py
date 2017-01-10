#!/usr/bin/python

import os
import sys
from pstep import PStep
import paramiko

cmd = sys.argv[1]
ps = PStep('CALVALUS')

# lc2-step ql noaa11 AVHRR_AC 1993 /calvalus/eodata/AVHRR_L1B/noaa11/1993 /calvalus/projects/lc/ql-noaa11-AVHRR_L1B/1993

if cmd == 'ql-orbit':

    variables = {
        'mission' : sys.argv[2],
        'sensor' : sys.argv[3],
        'year' : sys.argv[4],
        'input' : sys.argv[5],
        'output' : sys.argv[6],
        'bands' : 'counts_1,counts_2,counts_4'
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[4])
    ps.submit_request(request)
    
# lc2-step era-interim proba 2009-01-01 2009-01-31 /calvalus/eodata/PROBAV_S1_TOA/v2/2009/01 /calvalus/projects/lc/era-interim-proba/2009/01

elif cmd == 'era-interim':

    year = sys.argv[3][:4]
    month = sys.argv[3][5:7]
    variables = {
        'resolution' : sys.argv[2],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'input' : sys.argv[5][:-8],
        'output' : sys.argv[6],
        'year' : year,
        'month' : month
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + year + '-' + month)
    ps.submit_request(request)

# lc2-step sdr fr 2009-01-01 2009-01-31 default /calvalus/inventory/MER_FSG_1P/v2013/2009 /calvalus/eodata/MER_FSG_1P/v2013/2009/01 /calvalus/projects/lc/sdr-fr/2009/01 [/calvalus/projects/lc/sdr-fr/2009]

elif cmd == 'sdr':

    year = sys.argv[3][:4]
    month = sys.argv[3][5:7]
    template = { 'fr': 'sdr',
                 'rr': 'sdr',
                 'spot': 'sdr-spot',
                 'proba': 'sdr-proba',
                 'avhrr11': 'sdr-avhrr',
                 'avhrr14': 'sdr-avhrr',
                 'avhrr': 'sdr-avhrr',
                 'avhrr2': 'sdr-avhrr' }[sys.argv[2]]
    variables = {
        'resolution' : sys.argv[2],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'useUclCloudForShadow' : sys.argv[5]=='default',
        'inventory' : sys.argv[6],
        'input' : sys.argv[7][:-8],
        'output' : sys.argv[8],
        'year' : year,
        'month' : month
    }
    request = ps.apply_template(template, variables, sys.argv[2] + '-' + sys.argv[5] + '-' + year + '-' + month)
    ps.submit_request(request)

# lc2-step.py ncformat fr 2009-01-01 default /calvalus/projects/lc/sdr-fr/2009/01 /calvalus/projects/lc/sdr-fr-nc/2009/01

elif cmd == 'ncformat':

    year = sys.argv[3][:4]
    month = sys.argv[3][5:7]
    pattern = { 'fr': 'L2_of_MER_..._1P....${yyyy}${MM}${dd}_.*.seq',
                'rr': 'L2_of_MER_..._1P....${yyyy}${MM}${dd}_.*.seq',
                'avhrr11': 'L2_of_ao11${MM}${dd}.*.seq',
                'avhrr14': 'L2_of_ao14${MM}${dd}.*.seq',
                'spot': 'L2_of_V.KRNP____${yyyy}${MM}${dd}F.*.seq',
                'proba': 'L2_of_PROBAV_S1_TOA_......_${yyyy}${MM}${dd}.*.seq' }[sys.argv[2]]
    variables = {
        'resolution' : sys.argv[2],
        'input' : sys.argv[5],
        'output' : sys.argv[6],
        'year' : year,
        'month' : month,
        'pattern' : pattern
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + sys.argv[4] + '-' + year + '-' + month)
    ps.submit_request(request)
    
# lc2-step.py sr fr 2010-01-01 2010-01-07 default /calvalus/projects/lc/sdr-fr/2010 /calvalus/projects/lc/sr-fr-default/2010

elif cmd == 'sr':

    year = sys.argv[3][:4]
    pattern = { 'fr': 'L2_of_MER_..._1P....${yyyy}${MM}${dd}_.*.seq',
                'rr': 'L2_of_MER_..._1P....${yyyy}${MM}${dd}_.*.seq',
                'avhrr11': 'ao11${MM}${dd}.*.nc',
                'avhrr14': 'ao14${MM}${dd}.*.nc',
                'avhrr': 'L2_of_ao..${MM}${dd}.*.nc',
                'spot': 'L2_of_V.KRNP____${yyyy}${MM}${dd}F.*.seq',
                'proba': 'L2_of_PROBAV_S1_TOA_......_${yyyy}${MM}${dd}.*.seq' }[sys.argv[2]]
    variables = {
        'resolution' : sys.argv[2],
        'RESOLUTION' : { 'fr': 'FR',
                 'rr': 'RR',
                 'spot': 'SPOT',
                 'proba': 'PROBA',
                 'avhrr11': 'HRPT',
                 'avhrr14': 'HRPT',
                 'avhrr': 'HRPT' }[sys.argv[2]],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'filter' : sys.argv[5],
        'input' : sys.argv[6][:sys.argv[6].rfind('/')],
        'output' : sys.argv[7]+'/l3-',
        'year' : year,
        'pattern' : pattern
    }
    request = ps.apply_template('sr', variables, sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[5])
    ps.submit_request(request)

# lc2-step.py nccopy fr 2003-01-01 2003-01-31 default /calvalus/projects/lc/sr-fr-default/2003 /calvalus/projects/lc/sr-fr-nc-classic/2003

elif cmd == 'nccopy':

    year = sys.argv[3][:4]
    variables = {
        'resolution' : sys.argv[2],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'input' : sys.argv[6][:sys.argv[6].rfind('/')],
        'output' : sys.argv[7]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[5])
    ps.submit_request(request)

# lc2-step.py qll3 spot 2012-02-12 2012-02-18 7 default /calvalus/projects/lc/sr-spot-default/2012 /calvalus/projects/lc/ql-sr-spot-default/2012

elif cmd == 'qll3':

    year = sys.argv[3][:4]
    redband = { 'fr': 'sr_3_mean',
                'rr': 'sr_3_mean',
                'spot': 'sr_B0_mean',
                'proba': 'sr_1_mean',
                'avhrr11': 'sr_1_mean',
                'avhrr14': 'sr_1_mean',
                'avhrr': 'sr_1_mean' }
    greenband = { 'fr': 'sr_5_mean',
                  'rr': 'sr_5_mean',
                  'spot': 'sr_B2_mean',
                  'proba': 'sr_2_mean',
                  'avhrr11': 'sr_2_mean',
                  'avhrr14': 'sr_2_mean',
                  'avhrr': 'sr_2_mean' }
    blueband = { 'fr': 'sr_7_mean',
                 'rr': 'sr_7_mean',
                 'spot': 'sr_B3_mean',
                 'proba': 'sr_3_mean',
                 'avhrr11': 'bt_4_mean',
                 'avhrr14': 'bt_4_mean',
                 'avhrr': 'bt_4_mean' }

    variables = {
        'resolution' : sys.argv[2],
        'RESOLUTION' : { 'fr': 'FR',
                 'rr': 'RR',
                 'spot': 'SPOT',
                 'proba': 'PROBA',
                 'avhrr11': 'HRPT',
                 'avhrr14': 'HRPT',
                 'avhrr': 'HRPT' }[sys.argv[2]],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'periodLength' : sys.argv[5],
        'input' : sys.argv[7],
        'output' : sys.argv[8],
        'year' : year,
        'maskexpr' : 'current_pixel_state == 1 or current_pixel_state == 3',
        'redband' : redband[sys.argv[2]],
        'greenband' : greenband[sys.argv[2]],
        'blueband' : blueband[sys.argv[2]]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[6])
    ps.submit_request(request)

# lc2-step.py ql-avhrr-coverage noaa11 1993-01-01 1993-01-31 /calvalus/eodata/AVHRR_L1B/noaa11/1993/01 /calvalus/projects/lc/ql-avhrr-coverage/1993/01

elif cmd == 'ql-avhrr-coverage':

    year = sys.argv[3][:4]
    month = sys.argv[3][5:7]
    variables = {
        'platform' : sys.argv[2],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'input' : sys.argv[5][:-8],
        'output' : sys.argv[6],
        'year' : year,
        'month' : month
    }
    request = ps.apply_template(cmd, variables, year + '-' + month)
    ps.submit_request(request)

# lc2-step avhrr-idepix noaa14 1997-05-01 1997-05-31 /calvalus/eodata/AVHRR_L1B/noaa14/1997/05 /calvalus/projects/lc/avhrr-idepix/1997/05

elif cmd == 'avhrr-idepix':

    year = sys.argv[3][:4]
    month = sys.argv[3][5:7]
    variables = {
        'platform' : sys.argv[2],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'input' : sys.argv[5][:-8],
        'output' : sys.argv[6],
        'year' : year,
        'month' : month
    }
    request = ps.apply_template(cmd, variables, year + '-' + month)
    ps.submit_request(request)

# lc2-step.py seasonal-compositing fr 2009-12-03-P17W 2009-12-03 2010-04-01 120 /calvalus/eodata/MERIS_SR_FR/v1.0/2009 /calvalus/projects/lc/seasonal-fr/2009/2009-12-03-P17W

elif cmd == 'seasonal-compositing':

    if sys.argv[2] == 'fr' or sys.argv[2] == 'proba':
        rows = '64800'
    else:
        rows = '16200'
    variables = {
        'resolution' : sys.argv[2],
        'rows' : rows,
        'season' : sys.argv[3],
        'start' : sys.argv[4],
        'stop' : sys.argv[5],
        'period' : sys.argv[6],
        'input' : sys.argv[7][:-5],
        'output' : sys.argv[-1]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2]+'-'+sys.argv[3])
    ps.submit_request(request)

# lc2-step.py seasonal-formatting fr 2009-12-03-P17W 2009-12-03 2010-04-01 /calvalus/projects/lc/seasonal-fr/2009/2009-12-03-P17W /calvalus/projects/lc/seasonal-fr-geotiff/2009/2009-12-03-P17W

elif cmd == 'seasonal-formatting':

    variables = {
        'resolution' : sys.argv[2],
        'season' : sys.argv[3],
        'start' : sys.argv[4],
        'stop' : sys.argv[5],
        'input' : sys.argv[6],
        'output' : sys.argv[7]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2]+'-'+sys.argv[3])
    ps.submit_request(request)

# lc2-step.py qa-table fr 2009 /calvalus/eodata/MER_FRS_1P/v2013/2009 /calvalus/projects/lc/qa-fr/2009

elif cmd == 'qa-table':

    variables = {
        'resolution' : sys.argv[2],
        'year' : sys.argv[3],
        'input' : sys.argv[4],
        'output' : sys.argv[5]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2]+'-'+sys.argv[3])
    ps.submit_request(request)

# lc2-step.py mask noaa11 1992 /calvalus/eodata/AVHRR_L1B/noaa11/1992 /calvalus/projects/lc/mask-noaa11/1992

elif cmd == 'qa-mask':

    variables = {
        'resolution' : sys.argv[2],
        'year' : sys.argv[3],
        'input' : sys.argv[4],
        'output' : sys.argv[5]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + sys.argv[3])
    ps.submit_request(request)

# lc2-step qa-ql noaa11 1993 /calvalus/projects/lc/mask-noaa11/1992 /calvalus/projects/lc/qlm-noaa11/1992

elif cmd == 'qa-ql':

    variables = {
        'resolution' : sys.argv[2],
        'year' : sys.argv[3],
        'input' : sys.argv[4],
        'output' : sys.argv[5]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + sys.argv[3])
    ps.submit_request(request)
    
# lc2-step.py destitching noaa11 1993 05 31 /calvalus/eodata/AVHRR_L1B/noaa11/1993/05 /calvalus/projects/lc/destitching/noaa11-list/1993/05

elif cmd == 'destitching':

    variables = {
        'resolution' : sys.argv[2],
        'year' : sys.argv[3],
        'month' : sys.argv[4],
        'lastdayofmonth' : sys.argv[5],
        'input' : sys.argv[6][:-8],
        'output' : sys.argv[7]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2]+'-'+sys.argv[3]+'-'+sys.argv[4])
    ps.submit_request(request)

# lc2-step.py addheader noaa11 1993 05 /calvalus/projects/lc/destitching/noaa11-list/1993/05 /calvalus/projects/lc/destitching/noaa11-table/1993/05

elif cmd == 'addheader':

    resolution = sys.argv[2]
    year = sys.argv[3]
    month = sys.argv[4]
    csvlist = sys.argv[5] + '/part-r-00000'
    tableDir = sys.argv[6][:-8]
    table = tableDir + '/avhrr-' + resolution + '-' + year + '-' + month + '.csv'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('feeder01.bc.local', username=os.getlogin())
    ssh.exec_command('bash -c \'mkdir -p ' + tableDir + '; rm -f ' + table + '; echo "product	output	startLine	numLines	subsetX	subsetY	subsetWidth	subsetHeight" | cat - ' + csvlist + ' > ' + table + '\'')
    
# lc2-step.py addl2of noaa11 1993 05 /calvalus/projects/lc/destitching/noaa11-table/1993/05 /calvalus/projects/lc/destitching/noaa11-table2/1993/05

elif cmd == 'addl2of':

    resolution = sys.argv[2]
    year = sys.argv[3]
    month = sys.argv[4]
    tableDir = sys.argv[5][:-8]
    table = tableDir + '/avhrr-' + resolution + '-' + year + '-' + month + '.csv'
    table2Dir = sys.argv[6][:-8]
    table2 = table2Dir + '/avhrr-l2-' + resolution + '-' + year + '-' + month + '.csv'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('feeder01.bc.local', username=os.getlogin())
    ssh.exec_command('bash -c \'mkdir -p ' + table2Dir + '; rm -f ' + table2 + '; cat ' + table + ' | sed -e "s,ao,L2_of_L2_of_ao,g" -e "s,/calvalus/eodata/AVHRR_L1B/noaa\\(..\\)/\\(....\\)/\\(..\\)/..,/calvalus/projects/lc/ac-avhrr\\1-default-nc/\\2/\\3," -e "s,.l1b,.nc,g" > ' + table2 + '\'')
    
# lc2-step.py subsetting noaa11 1993 05 /calvalus/eodata/AVHRR_L1B/noaa11/1993/05 /calvalus/projects/lc/destitching/noaa11-table/1993/05 /calvalus/projects/lc/destitching/noaa11-albedo2/1993/05

elif cmd == 'subsetting':

    variables = {
        'resolution' : sys.argv[2],
        'year' : sys.argv[3],
        'month' : sys.argv[4],
        'table' : sys.argv[6][:-7] + 'avhrr-' + sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[4] + '.csv',
        'output' : sys.argv[7]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2]+'-'+sys.argv[3]+'-'+sys.argv[4])
    ps.submit_request(request)

# lc2-step.py subsetting2 noaa14 1996 06 /calvalus/projects/lc/ac-avhrr14-default-nc/1996/06 /calvalus/projects/lc/destitching/noaa14-table2/1996/06 /calvalus/projects/lc/ac-subsets-noaa14/1996/06

elif cmd == 'subsetting2':

    variables = {
        'resolution' : sys.argv[2],
        'year' : sys.argv[3],
        'month' : sys.argv[4],
        'table' : sys.argv[6][:-7] + 'avhrr-l2-' + sys.argv[2] + '-' + sys.argv[3] + '-' + sys.argv[4] + '.csv',
        'output' : sys.argv[7]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2]+'-'+sys.argv[3]+'-'+sys.argv[4])
    ps.submit_request(request)

# lc2-step.py correlating noaa11 1993 05 /calvalus/projects/lc/destitching/noaa11-albedo2/1993/05 /calvalus/projects/lc/destitching/noaa11-tiepoints/1993/05

elif cmd == 'correlating':

    variables = {
        'resolution' : sys.argv[2],
        'year' : sys.argv[3],
        'month' : sys.argv[4],
        'input' : sys.argv[5],
        'output' : sys.argv[6]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2]+'-'+sys.argv[3]+'-'+sys.argv[4])
    ps.submit_request(request)

# lc2-step.py warping noaa14 1996 06 /calvalus/projects/lc/ac-subsets-noaa14/1996/06 /calvalus/projects/lc/destitching/noaa14-tiepoints/1996/06 /calvalus/projects/lc/ac-warped-noaa14/1996/06

elif cmd == 'warping':

    variables = {
        'resolution' : sys.argv[2],
        'year' : sys.argv[3],
        'month' : sys.argv[4],
        'input' : sys.argv[5],
        'tiepoints' : sys.argv[6],
        'output' : sys.argv[7]
    }
    request = ps.apply_template(cmd, variables, sys.argv[2]+'-'+sys.argv[3]+'-'+sys.argv[4])
    ps.submit_request(request)

# lc2-step lcac noaa14 1996-06-01 1996-06-30 default /calvalus/projects/lc/sdr-noaa14-default-nc/1996/06 /calvalus/projects/lc/ac-noaa14-default-nc/1996/06

elif cmd == 'lcac':

    year = sys.argv[3][:4]
    month = sys.argv[3][5:7]
    variables = {
        'resolution' : sys.argv[2],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'input' : sys.argv[6],
        'output' : sys.argv[7],
        'year' : year,
        'month' : month
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + year + '-' + month)
    ps.submit_request(request)

# lc2-step qamerge noaa14 1996-06-01 1996-06-30 /calvalus/projects/lc/ac-noaa14-default-nc/1996/06 /calvalus/projects/lc/ac-noaa14-default-qa/1996/06

elif cmd == 'qamerge':

    year = sys.argv[3][:4]
    month = sys.argv[3][5:7]
    variables = {
        'resolution' : sys.argv[2],
        'start' : sys.argv[3],
        'stop' : sys.argv[4],
        'input' : sys.argv[6],
        'output' : sys.argv[7],
        'year' : year,
        'month' : month
    }
    request = ps.apply_template(cmd, variables, sys.argv[2] + '-' + year + '-' + month)
    ps.submit_request(request)

else:
    print 'unknown command', cmd
    sys.exit(1)
