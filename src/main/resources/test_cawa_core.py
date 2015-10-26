import os

__author__ = 'olafd'
import unittest
import time

import numpy

# import snappy

# import cawa_core_debug as cawa
import cawa_core as cawa


class test_cawa_core(unittest.TestCase):
    def setUp(self):
        self.cawa = cawa.cawa_core(os.path.join('.', 'luts', 'wadamo_core_meris.json'))
        # self.cawa = cawa.cawa_core(os.path.join('.', 'luts', 'wadamo_core_modis_terra.json'))

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

        t_ave = 0.0
        for i in range(1000):
            t1 = time.clock() * 1000
            tcwv_result = self.cawa.estimator(inp, 0, 0)['tcwv']
            # print('pixel tcwv result: ', tcwv_result)
            self.assertAlmostEqual(tcwv_result, 43.52, delta=0.1)
            # self.assertAlmostEqual(self.cawa.estimator(inp, 0, 0, False)['tcwv'], 43.52, delta=0.1)   # almost twice as slow
            t2 = time.clock() * 1000
            # print('TCWV estimator time (ms) for one pixel: ', (t2 - t1))
            t_ave += (t2-t1)
        print('TCWV estimator average time (ms) for one pixel: ', t_ave/1000.0)


    @unittest.skip("skipping test...")
    def test_estimator_modis(self):
        inp = {'tmp': 303.
            , 'prs': 1003.
            , 'suz': 9.7968997955322270
            , 'vie': 46.12860107421875
            , 'azi': 18.
            , 'aot': {'2': 0.1
                    , '5': 0.08
                    , '17': 0.1
                    , '18': 0.1
                    , '19': 0.1
                      }
            , 'sig_aot': {'2': 0.1
                    , '5': 0.08
                    , '17': 0.1
                    , '18': 0.1
                    , '19': 0.1
                      }
            , 'rtoa': {'2': 0.2/numpy.pi
                    , '5': 0.205/numpy.pi
                    , '17': 0.158/numpy.pi
                    , '18': 0.06/numpy.pi
                    , '19': 0.094/numpy.pi
                      }
               }
        t1 = time.clock() * 1000
        tcwv_result = self.cawa.estimator(inp, 0, 0)['tcwv']
        print('pixel MODIS tcwv result: ', tcwv_result)
        self.assertAlmostEqual(tcwv_result, 15.26, delta=0.1)
        t2 = time.clock() * 1000
        print('TCWV estimator time (ms) for one pixel MODIS: ', (t2 - t1))

    @unittest.skip("skipping test...")
    def test_flags(self):
        tcwvData = numpy.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=numpy.float32)
        tcwvLow = tcwvData < 2.0
        tcwvHigh = tcwvData > 3.0
        tcwvFlags = tcwvLow + 2 * tcwvHigh
        print('tcwvLow: ', tcwvLow)
        print('tcwvHigh: ', tcwvHigh)
        print('flags: ', tcwvFlags)
        tcwvFlags2 = numpy.empty(5, dtype=numpy.uint8)
        tcwvFlags2 = tcwvLow + 2 * tcwvHigh
        t1 = time.clock() * 1000
        # tcwvFlags2 = tcwvFlags2.astype(numpy.uint8, copy=False)
        tcwvFlags2 = tcwvFlags2.view(numpy.uint8)
        t2 = time.clock() * 1000
        print('astype: ', (t2 - t1))
        print('flags2: ', tcwvFlags2)


print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(test_cawa_core)
unittest.TextTestRunner(verbosity=2).run(suite)

