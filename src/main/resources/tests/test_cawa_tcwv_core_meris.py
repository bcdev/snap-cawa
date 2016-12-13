import os
import sys

import unittest
import time

import numpy as np


# noinspection PyUnresolvedReferences
class TestCawaCoreMeris(unittest.TestCase):
    def setUp(self):
        parent_dir = os.path.dirname(os.path.normpath(os.path.dirname(__file__)))
        sys.path.append(parent_dir + '/libs')

        import cawa_tcwv_core as cawa_core
        import cawa_tcwv_land as cawa_land
        import cawa_tcwv_ocean as cawa_ocean

        land_lut = os.path.join(parent_dir, 'luts', 'land', 'land_core_meris.nc4')
        ocean_lut = os.path.join(parent_dir, 'luts', 'ocean', 'ocean_core_meris.nc4')

        self.cawa_core = cawa_core.CawaTcwvCore(land_lut, ocean_lut)
        self.cawa_land = cawa_land.CawaTcwvLandCore(os.path.join(parent_dir, 'luts', 'land', 'land_core_meris.nc4'))
        self.cawa_ocean = cawa_ocean.CawaTcwvOceanCore(os.path.join(parent_dir, 'luts', 'ocean', 'ocean_core_meris.nc4'))


    # @unittest.skip("skipping test...")
    def test_estimator_meris_land(self):
        inp = {'suz': 30., 'vie': 20., 'azi': 170.,
               'amf': 1. / np.cos(40. * np.pi / 180.) + 1. / np.cos(10. * np.pi / 180.),
               'prs': 1005, 'aot': 0.1, 'tmp': 280.,
               'rtoa': {'13': 0.04228669, '14': 0.04442161, '15': 0.031},
               'prior_al0': 0.13, 'prior_al1': 0.13, 'prior_tcwv': 15.}

        t_ave = 0.0
        for i in range(1000):
            t1 = time.clock() * 1000
            tcwv_result = self.cawa_land.estimator(inp)['tcwv']
            # print('pixel tcwv result: ', tcwv_result)
            self.assertAlmostEqual(tcwv_result, 24.17, delta=0.01)
            t2 = time.clock() * 1000
            # print('TCWV land estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('TCWV land estimator average time (ms) for one pixel: ', t_ave/1000.0)

    # @unittest.skip("skipping test...")
    def test_estimator_meris_land_via_core(self):
        inp = {'suz': 30., 'vie': 20., 'azi': 170.,
               'amf': 1. / np.cos(40. * np.pi / 180.) + 1. / np.cos(10. * np.pi / 180.),
               'prs': 1005, 'aot': 0.1, 'tmp': 280.,
               'rtoa': {'13': 0.04228669, '14': 0.04442161, '15': 0.031},
               'prior_al0': 0.13, 'prior_al1': 0.13, 'prior_tcwv': 15.}

        t_ave = 0.0
        for i in range(1000):
            t1 = time.clock() * 1000
            tcwv_result = self.cawa_core.compute_pixel_meris(inp, 128, 0)['tcwv']
            # print('pixel tcwv result: ', tcwv_result)
            self.assertAlmostEqual(tcwv_result, 24.17, delta=0.01)
            t2 = time.clock() * 1000
            # print('TCWV land estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('TCWV land estimator average time (ms) for one pixel: ', t_ave/1000.0)

    # @unittest.skip("skipping test...")
    def test_estimator_meris_ocean(self):
        inp={'suz':10.,'vie':40.,'azi':170.,
             'amf':1./np.cos(40.*np.pi/180.)+1./np.cos(10.*np.pi/180.),
             'rtoa':{'13':0.0045663,'14':0.00440355,'15':0.00356704375818},
             'prior_wsp':7.5,'prior_aot':0.15,'prior_tcwv':15.}

        t_ave = 0.0
        for i in range(1000):
            t1 = time.clock() * 1000
            tcwv_result = self.cawa_ocean.estimator(inp)['tcwv']
            # print('pixel tcwv result: ', tcwv_result)
            self.assertAlmostEqual(tcwv_result, 17.88, delta=0.01)
            t2 = time.clock() * 1000
            # print('TCWV ocean estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('TCWV ocean estimator average time (ms) for one pixel: ', t_ave/1000.0)

    def test_estimator_meris_ocean_via_core(self):
        inp={'suz':10.,'vie':40.,'azi':170.,
             'amf':1./np.cos(40.*np.pi/180.)+1./np.cos(10.*np.pi/180.),
             'rtoa':{'13':0.0045663,'14':0.00440355,'15':0.00356704375818},
             'prior_wsp':7.5,'prior_aot':0.15,'prior_tcwv':15.}

        t_ave = 0.0
        for i in range(1000):
            t1 = time.clock() * 1000
            tcwv_result = self.cawa_core.compute_pixel_meris(inp, 0, 0)['tcwv']
            # print('pixel tcwv result: ', tcwv_result)
            self.assertAlmostEqual(tcwv_result, 17.88, delta=0.01)
            t2 = time.clock() * 1000
            # print('TCWV ocean estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('TCWV ocean estimator average time (ms) for one pixel: ', t_ave/1000.0)

print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(TestCawaCoreMeris)
unittest.TextTestRunner(verbosity=2).run(suite)
