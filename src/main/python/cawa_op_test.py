__author__ = 'olafd'
import os
import unittest

import cawa_core as caw
import cawa_op


class test_cawa_operator(unittest.TestCase):
    def setUp(self):
        self.cw = caw.cawa_core(os.path.join('.','luts','wadamo_core_meris.json'))
        self.op = cawa_op.CawaOp()

    def test_estimator_meris(self):
        inp={'tmp':273.
            ,'prs':900.
            ,'suz':9.7968997955322270
            ,'vie':46.12860107421875
            ,'azi':18.
            ,'aot': {'13':0.1
            , '14':0.1
            , '15':0.095
                    }
            ,'sig_aot': {'13':0.1
            , '14':0.1
            , '15':0.095
                        }
            ,'rtoa':{'13':0.0313
            , '14':0.0329
            , '15':0.0204
                    }
        }
        # directly from python:
        self.assertAlmostEqual(self.cw.estimator(inp)['tcwv'],43.52,delta=0.1)
        # from operator method:
        # self.assertAlmostEqual(self.op.getTcwv(inp),43.52,delta=0.1)
        self.assertAlmostEqual(self.op.getTcwv(self.cw, inp),43.52,delta=0.1)

#unittest.main()
print 'Testing the org.esa.snap.cawa operator'
suite = unittest.TestLoader().loadTestsFromTestCase(test_cawa_operator)
unittest.TextTestRunner(verbosity=2).run(suite)

