import os
import sys

import unittest
import time

import numpy as np


# noinspection PyUnresolvedReferences
class TestCawaCoreModis(unittest.TestCase):
    def setUp(self):
        parent_dir = os.path.dirname(os.path.normpath(os.path.dirname(__file__)))
        sys.path.append(parent_dir + '/libs')

        import cawa_tcwv_core as cawa_core
        import cawa_tcwv_land as cawa_land
        import cawa_tcwv_ocean as cawa_ocean

        land_lut = os.path.join(parent_dir, 'luts', 'land', 'land_core_modis_terra.nc4')
        ocean_lut = os.path.join(parent_dir, 'luts', 'ocean', 'ocean_core_modis_terra.nc4')

        self.cawa_core = cawa_core.CawaTcwvCore(land_lut, ocean_lut)
        self.cawa_land = cawa_land.CawaTcwvLandCore(os.path.join(parent_dir, 'luts', 'land', 'land_core_modis_terra.nc4'))
        self.cawa_ocean = cawa_ocean.CawaTcwvOceanCore(os.path.join(parent_dir, 'luts', 'ocean', 'ocean_core_modis_terra.nc4'))


    # @unittest.skip("skipping test...")
    def test_estimator_modis_via_core(self):
        inp = {'tmp': 303.,
               'prs': 1003.,
               'suz': 9.7969,
               'vie': 46.1286,
               'amf':1./np.cos(46.1286*np.pi/180.)+1./np.cos(9.7969*np.pi/180.),
               'azi': 18.,
               'aot': {'2': 0.1, '5': 0.08, '17': 0.1, '18': 0.1, '19': 0.1},
               'sig_aot': {'2': 0.1, '5': 0.08, '17': 0.1, '18': 0.1, '19': 0.1},
               'prior_wsp':7.5,'prior_aot':0.15,'prior_tcwv':15.,
               'rtoa': {'2': 0.2 / np.pi, '5': 0.205 / np.pi, '17': 0.158 / np.pi, '18': 0.06 / np.pi, '19': 0.094 / np.pi}
               }
        t1 = time.clock() * 1000
        # tcwv_result = self.cawa_land.estimator(inp, 0, 0)['tcwv']
        tcwv_result = self.cawa_core.compute_pixel_meris(inp, 0, 0)['tcwv']
        print('pixel MODIS tcwv result: ', tcwv_result)
        self.assertAlmostEqual(tcwv_result, 15.26, delta=0.1)
        t2 = time.clock() * 1000
        print('TCWV estimator time (ms) for one pixel MODIS: ', (t2 - t1))

print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(TestCawaCoreModis)
unittest.TextTestRunner(verbosity=2).run(suite)
