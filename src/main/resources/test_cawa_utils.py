import os

__author__ = 'olafd'
import unittest
import time

import numpy

# import snappy

import cawa_utils as cu


class test_cawa_utils(unittest.TestCase):
    def setUp(self):
        bla = 0
        self.cu = cu.cawa_utils()

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

    def test_mask(self):
        inputData = numpy.array([3, 12, 6, 16, 36, 64], dtype=numpy.int32)
        l1DummyData = numpy.array([0, 0, 0, 0, 0, 0], dtype=numpy.int32)
        mask = numpy.empty(6, dtype=numpy.uint8)
        for i in range(inputData.shape[0]):
            mask[i] = self.cu.calculate_pixel_mask_array(i, inputData, l1DummyData)

        self.assertItemsEqual(mask, [1, 1, 1, 0, 0, 0])
        print('mask: ', mask)
        print('inputData: ', inputData)
        valid = mask == 0
        print('valid: ', valid)
        print('inputData[valid]: ', inputData[valid])

        # inp = {{'tmp': 303., 'prs': 1003.}, {'tmp': 6749., 'prs': 2005.}}
        # print('inp[0]: ', inp.values()[0])
        # print('inp[1]: ', inp.values()[1])


print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(test_cawa_utils)
unittest.TextTestRunner(verbosity=2).run(suite)

