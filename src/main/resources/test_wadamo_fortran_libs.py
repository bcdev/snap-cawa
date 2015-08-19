import os
import zipfile
import sys

__author__ = 'olafd'
import unittest

import numpy.f2py as f2py

import shared_libs

# import snappy


class test_wadamo_fortran_libs(unittest.TestCase):
    # def setUp(self):
    #     bla = 0

    def test_extract_shared_lib_to_python(self):
        resource_root = os.path.dirname(__file__)
        print('Python module location parent: ' + resource_root)
        print('sys executable: ' + sys.executable)
        python_root = os.path.dirname(sys.executable)
        print('Python install dir: ' + python_root)

        with zipfile.ZipFile(resource_root) as zf:
            wadamo_ftn_poly = zf.extract('shared_libs/win32/f2py/wadamo_poly.pyd', os.path.join(python_root, 'cawa'))
            print('LUT json file: ' + wadamo_ftn_poly)


    # @unittest.skip("skipping test...")
    # def test_polyexp_fortran(self):
    #     x = 2.0
    #     par = 3.0
    #     pot = 0.333333
    #     polyexp_f = wadamo_poly.polyexp(x, par, pot)
    #     print('polyexp_f: ' + str(polyexp_f))

print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(test_wadamo_fortran_libs)
unittest.TextTestRunner(verbosity=2).run(suite)

