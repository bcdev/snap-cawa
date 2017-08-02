import os
import sys

import unittest
import time

import numpy as np

import cawa_utils as cu


# noinspection PyUnresolvedReferences
class TestCawaCtpCoreOlci(unittest.TestCase):
    def setUp(self):
        parent_dir = os.path.dirname(os.path.normpath(os.path.dirname(__file__)))
        sys.path.append(parent_dir + '/libs')

        import cawa_ctp_olci_core as cawa_ctp_core
        import cawa_ctp as cawa_ctp

        ctp_lut = os.path.join(parent_dir, 'luts', 'cloud_core_olci.nc4')

        self.cawa_core = cawa_ctp_core.CawaCtpOlciCore(ctp_lut)
        self.cawa_ctp = cawa_ctp.CawaCtpCore(os.path.join(parent_dir, 'luts', 'cloud_core_olci.nc4'))

        # test input from
        # ../ubuntu_shared/cawa/ctp/subset_2x2_of_S3A_OL_1_EFR____20160526T100432_20160526T100632_20161219T151643_
        #                           0119_004_293______MR1_R_NT_002,
        # pixel 100/320 in original subset_0_of_S3A_OL_1_EFR____20160526T100432_20160526T100632_20161219T151643_
        #                           0119_004_293______MR1_R_NT_002
        self.inp = {'azi': 20.539501,
               'vie': 36.213432,
               'alb': 0.19606047930815135,
               'rtoa': {'13': 0.055332646, '12': 0.17908783, '15': 0.16216847, '14': 0.095478348},
               'suz': 30.639153,
            'dwl': 0.10369873}


    #@unittest.skip("skipping test...")
    def test_estimator_olci_ctp(self):
        t_ave = 0.0
        for i in range(1):
            t1 = time.clock() * 1000
            ctp_result = self.cawa_ctp.estimator(self.inp)['ctp']
            #print('pixel olci ctp result: ', ctp_result)
            self.assertAlmostEqual(ctp_result, 795.5249, delta=0.001)
            t2 = time.clock() * 1000
            #print('CTP OLCI estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('CTP OLCI estimator average time (ms) for one pixel: ', t_ave/1000.0)

    #@unittest.skip("skipping test...")
    def test_estimator_olci_ctp_via_core(self):
        t_ave = 0.0
        for i in range(1):
            t1 = time.clock() * 1000
            ctp_result = self.cawa_core.compute_pixel_ctp_olci(self.inp, cu.CAWA_OLCI_IDEPIX_CLOUD)['ctp']
            #print('pixel olci ctp result: ', ctp_result)
            self.assertAlmostEqual(ctp_result, 821.02777, delta=0.001)
            t2 = time.clock() * 1000
            #print('CTP OLCI estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('CTP OLCI estimator (via core) average time (ms) for one pixel: ', t_ave/1000.0)

print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(TestCawaCtpCoreOlci)
unittest.TextTestRunner(verbosity=2).run(suite)
