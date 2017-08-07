import os
import sys

import unittest

class TestHello(unittest.TestCase):
    def setUp(self):
        print 'bla'

    def test_hello(self):
        parent_dir = os.path.dirname(os.path.normpath(os.path.dirname(__file__)))
        sys.path.append(parent_dir + '/lib-python')
        lib_dir = os.path.join(parent_dir, 'lib-python')
        sys.path.append(lib_dir)
        print 'sys.path: ', sys.path
        print 'lib_dir: ', lib_dir
        print 'os.environ[PYTHONPATH]: ', os.environ['PYTHONPATH']
        import hello

        print hello.__doc__
        print hello.foo.__doc__
        hello.foo(4)

print 'Testing org.esa.snap.cawa core'
suite = unittest.TestLoader().loadTestsFromTestCase(TestHello)
unittest.TextTestRunner(verbosity=2).run(suite)
