import os
import sys

import unittest
import time

import numpy as np

import cawa_utils as cu


# noinspection PyUnresolvedReferences
class TestCawaCtpCoreMeris(unittest.TestCase):
    def setUp(self):
        parent_dir = os.path.dirname(os.path.normpath(os.path.dirname(__file__)))
        sys.path.append(parent_dir + '/libs')

        import cawa_ctp_meris_core as cawa_ctp_core
        import cawa_ctp as cawa_ctp

        ctp_lut = os.path.join(parent_dir, 'luts', 'cloud_core_meris.nc4')

        self.cawa_core = cawa_ctp_core.CawaCtpMerisCore(ctp_lut)
        self.cawa_ctp = cawa_ctp.CawaCtpCore(os.path.join(parent_dir, 'luts', 'cloud_core_meris.nc4'))

        # test input from
        # ../ubuntu_shared/cawa/ctp/subset_2x2_of_MER_RR__1PRACR20041229_090630_000026192033_00222_14805_0000_IDEPIX.dim,
        # pixel 924/2359 in original MER_RR__1PRACR20041229_090630_000026192033_00222_14805_0000
        self.inp = {'azi': 128.91507,
               'vie': 28.734968,
               'alb': 0.49799361744270443,
               'rtoa': {'11': 0.041544202204865412, '10': 0.13373079095734028},
               'prs': 1009.1498,
               'suz': 57.238201,
               'dwl': 1.213444213656885}


    #@unittest.skip("skipping test...")
    def test_estimator_meris_ctp(self):
        t_ave = 0.0
        for i in range(1):
            t1 = time.clock() * 1000
            ctp_result = self.cawa_ctp.estimator(self.inp)['ctp']
            #print('pixel meris ctp result: ', ctp_result)
            self.assertAlmostEqual(ctp_result, 821.02777, delta=0.001)
            t2 = time.clock() * 1000
            #print('CTP MERIS estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('CTP MERIS estimator average time (ms) for one pixel: ', t_ave/1000.0)

    @unittest.skip("skipping test...")
    def test_estimator_meris_ctp_via_core(self):
        t_ave = 0.0
        for i in range(1000):
            t1 = time.clock() * 1000
            ctp_result = self.cawa_core.compute_pixel_ctp_meris(self.inp, cu.CAWA_MERIS_IDEPIX_CLOUD)['ctp']
            #print('pixel meris ctp result: ', ctp_result)
            self.assertAlmostEqual(ctp_result, 821.02777, delta=0.001)
            t2 = time.clock() * 1000
            #print('CTP MERIS estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('CTP MERIS estimator (via core) average time (ms) for one pixel: ', t_ave/1000.0)

print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(TestCawaCtpCoreMeris)
unittest.TextTestRunner(verbosity=2).run(suite)
