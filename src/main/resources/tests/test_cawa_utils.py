import os
import sys

import unittest
import time

import numpy as np
import cawa_utils as cu


# noinspection PyUnresolvedReferences
class TestCawaUtils(unittest.TestCase):
    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.normpath(os.path.dirname(__file__)))
        print('parentDir: ', self.parent_dir)
        sys.path.append(self.parent_dir + '/libs')

    def test_read_sun_spectral_fluxes_csv(self):
        spectral_fluxes_input_path = os.path.join(self.parent_dir, 'meris_sun_spectral_flux_rr_10_11.txt')
        spectral_fluxes_table = cu.CawaUtils.get_table_from_csvfile(spectral_fluxes_input_path, ',', "")

        spectral_flux_10 = np.array(spectral_fluxes_table['E0_band10'])
        spectral_flux_11 = np.array(spectral_fluxes_table['E0_band11'])
        self.assertEqual(len(spectral_flux_10), 925)
        self.assertEqual(len(spectral_flux_11), 925)
        self.assertAlmostEqual(float(spectral_flux_10[0]), 1266.148, delta=0.001)
        self.assertAlmostEqual(float(spectral_flux_10[621]), 1265.939, delta=0.001)
        self.assertAlmostEqual(float(spectral_flux_10[924]), 1265.985, delta=0.001)
        self.assertAlmostEqual(float(spectral_flux_11[0]), 1249.929, delta=0.001)
        self.assertAlmostEqual(float(spectral_flux_11[374]), 1249.586, delta=0.001)
        self.assertAlmostEqual(float(spectral_flux_11[924]), 1251.573, delta=0.001)
        print('done test_read_sun_spectral_fluxes_csv')


print 'Testing org.esa.snap.cawa utils'
suite = unittest.TestLoader().loadTestsFromTestCase(TestCawaUtils)
unittest.TextTestRunner(verbosity=2).run(suite)
