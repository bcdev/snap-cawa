import os

import unittest
import time

import numpy as np

import cawa_tcwv_core as cawa_core
import cawa_tcwv_land as cawa_land
import cawa_tcwv_ocean as cawa_ocean


class test_cawa_core(unittest.TestCase):
    def setUp(self):
        land_lut = os.path.join('../', 'luts', 'land', 'land_core_meris.nc4')
        ocean_lut = os.path.join('../', 'luts', 'ocean', 'ocean_core_meris.nc4')
        self.cawa_core = cawa_core.cawa_tcwv_core(land_lut, ocean_lut)
        self.cawa_land = cawa_land.cawa_tcwv_land_core(os.path.join('../', 'luts', 'land', 'land_core_meris.nc4'))
        self.cawa_ocean = cawa_ocean.cawa_tcwv_ocean_core(os.path.join('../', 'luts', 'ocean', 'ocean_core_meris.nc4'))

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
            tcwv_result = self.cawa_core.compute_pixel(inp, 128, 0)['tcwv']
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
            tcwv_result = self.cawa_core.compute_pixel(inp, 0, 0)['tcwv']
            # print('pixel tcwv result: ', tcwv_result)
            self.assertAlmostEqual(tcwv_result, 17.88, delta=0.01)
            t2 = time.clock() * 1000
            # print('TCWV ocean estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('TCWV ocean estimator average time (ms) for one pixel: ', t_ave/1000.0)

    # @unittest.skip("skipping test...")
    # def test_estimator_modis(self):
    #     inp = {'tmp': 303.,
    #            'prs': 1003.,
    #            'suz': 9.7968997955322270,
    #            'vie': 46.12860107421875,
    #            'azi': 18.,
    #            'aot': {'2': 0.1, '5': 0.08, '17': 0.1, '18': 0.1, '19': 0.1},
    #            'sig_aot': {'2': 0.1, '5': 0.08, '17': 0.1, '18': 0.1, '19': 0.1},
    #            'rtoa': {'2': 0.2 / np.pi, '5': 0.205 / np.pi, '17': 0.158 / np.pi, '18': 0.06 / np.pi, '19': 0.094 / np.pi}
    #            }
    #     t1 = time.clock() * 1000
    #     tcwv_result = self.cawa_land.estimator(inp, 0, 0)['tcwv']
    #     print('pixel MODIS tcwv result: ', tcwv_result)
    #     self.assertAlmostEqual(tcwv_result, 15.26, delta=0.1)
    #     t2 = time.clock() * 1000
    #     print('TCWV estimator time (ms) for one pixel MODIS: ', (t2 - t1))

print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(test_cawa_core)
unittest.TextTestRunner(verbosity=2).run(suite)
