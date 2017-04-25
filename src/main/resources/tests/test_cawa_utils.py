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
        spectral_fluxes_input_path = os.path.join(self.parent_dir, 'luts/meris_sun_spectral_flux_rr_10_11.txt')
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

    def test_get_meris_rr_product_datestring(self):
        product_name = 'bla__1PRACR20041229_090630_000026192033_00222_14805_0000_IDEPIX.dim'
        datestring = cu.CawaUtils.get_meris_rr_product_datestring(product_name)
        self.assertIsNone(datestring)

        product_name = 'MER_RR__1PRACR20041229_090630_000026192033_00222_14805_0000_IDEPIX.NC'
        datestring = cu.CawaUtils.get_meris_rr_product_datestring(product_name)
        self.assertEqual('20041229', datestring)

        product_name = 'L2_of_MER_RR__1PRACR19971023_090630_000026192033_00222_14805_0000_IDEPIX.nc'
        datestring = cu.CawaUtils.get_meris_rr_product_datestring(product_name)
        self.assertEqual('19971023', datestring)

        product_name = 'subset_0_of_MER_RR__1PRACR19971023_090630_000026192033_00222_14805_0000.nc'
        datestring = cu.CawaUtils.get_meris_rr_product_datestring(product_name)
        self.assertEqual('19971023', datestring)
        print('done test_get_meris_rr_product_datestring')

    def test_get_olci_product_datestring(self):
        product_name = \
            'bla_20160428T135236_20160428T135436_20161217T072041_0119_003_281______MR1_R_NT_002.SEN3_IDEPIX.dim'
        datestring = cu.CawaUtils.get_olci_product_datestring(product_name)
        self.assertIsNone(datestring)

        product_name = \
            'S3A_OL_1_EFR____20160116T135236_20160428T135436_20161217T072041_0119_003_281______MR1_R_NT_002.SEN3_IDEPIX.NC'
        datestring = cu.CawaUtils.get_olci_product_datestring(product_name)
        self.assertEqual('20160116', datestring)

        product_name = \
            'L2_of_S3A_OL_1_EFR____19971023T135236_20160428T135436_20161217T072041_0119_003_281______MR1_R_NT_002.SEN3_IDEPIX.nc'
        datestring = cu.CawaUtils.get_olci_product_datestring(product_name)
        self.assertEqual('19971023', datestring)

        product_name = \
            'subset_0_of_S3A_OL_1_EFR____19980308T135236_20160428T135436_20161217T072041_0119_003_281______MR1_R_NT_002.SEN3_IDEPIX.nc'
        datestring = cu.CawaUtils.get_olci_product_datestring(product_name)
        self.assertEqual('19980308', datestring)
        print('done test_get_olci_product_datestring')


    def test_get_doy_from_yyyymmdd(self):
        datestring = '20000101'
        doy = cu.CawaUtils.get_doy_from_yyyymmdd(datestring)
        self.assertEqual(1, int(doy))

        datestring = '20041229'
        doy = cu.CawaUtils.get_doy_from_yyyymmdd(datestring)
        self.assertEqual(364, int(doy))


print 'Testing org.esa.snap.cawa utils'
suite = unittest.TestLoader().loadTestsFromTestCase(TestCawaUtils)
unittest.TextTestRunner(verbosity=2).run(suite)
