import os
import time

__author__ = 'olafd'

import cawa_core_debug
import profile

def bla():
    cawa = cawa_core_debug.cawa_core_debug(os.path.join('.', 'luts', 'wadamo_core_meris.json'))

    inp = {'tmp': 273.
        , 'prs': 900.
        , 'suz': 9.7968997955322270
        , 'vie': 46.12860107421875
        , 'azi': 18.
        , 'aot': {'13': 0.1
        , '14': 0.1
        , '15': 0.095
    }
        , 'sig_aot': {'13': 0.1
        , '14': 0.1
        , '15': 0.095
    }
        , 'rtoa': {'13': 0.0313
        , '14': 0.0329
        , '15': 0.0204
    }
    }
    t1 = time.clock() * 1000
    print('pixel tcwv result: ', cawa.estimator(inp)['tcwv'])
    t2 = time.clock() * 1000
    print('TCWV estimator time (ms) for one pixel: ', (t2 - t1))

profile.run('bla()')
