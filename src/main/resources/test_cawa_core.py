import os

__author__ = 'olafd'
import unittest
import time

import numpy

# import snappy

import cawa_core as cawa


class test_cawa_core(unittest.TestCase):
    def setUp(self):
        bla = 0
        self.cawa = cawa.cawa_core(os.path.join('.', 'luts', 'wadamo_core_meris.json'))

    # @unittest.skip("skipping test...")
    # def test_call_op(self):
    #     # todo: this test does not yet work!
    #     ifile = 'F:\olafd\wadamo\MER_RR_SUBSET_radiometry.dim'
    #     ofile = 'F:\olafd\wadamo\MER_RR_SUBSET_radiometry_PYWADAMO_2.dim'
    #
    #     temperature = 303.0
    #     pressure = 1003.0
    #
    #     parameters = {
    #         'temperature':temperature
    #         ,'pressure':pressure
    #     }
    #
    #     source_product = snappy.ProductIO.readProduct(ifile)
    #     # target_product = snappy.GPF.createProduct('cawa_op', parameters, source_product)
    #     target_product = snappy.GPF.createProduct('cawa_op', None, source_product)
    #     snappy.ProductIO.writeProduct(target_product, ofile, 'BEAM-DIMAP')


    # @unittest.skip("skipping test...")
    def test_estimator_meris(self):
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
        self.assertAlmostEqual(self.cawa.estimator(inp)['tcwv'], 43.52, delta=0.1)
        # self.assertAlmostEqual(self.wd.estimator(inp, False)['tcwv'], 43.52, delta=0.1)   # almost twice as slow
        t2 = time.clock() * 1000
        print('TCWV estimator time (ms) for one pixel: ', (t2 - t1))


print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(test_cawa_core)
unittest.TextTestRunner(verbosity=2).run(suite)

