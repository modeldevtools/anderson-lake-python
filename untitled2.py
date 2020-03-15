# -*- coding: utf-8 -*-
import unittest
import numpy as np

from pricers import anderson_lake
from integration import ExpSinhQuadrature
from models import HestonModel
from options import EuropeanCallOption

class TestAndersonLake(unittest.TestCase):
    def setUp(self):
        self.scheme = ExpSinhQuadrature(0.5, 1e-8, 100)
    
    def test_atm(self):
        model = HestonModel(100, 0.1197**2, 1.98937, 0.108977**2, 0.33147, \
                            0.0258519, 0)
        option = EuropeanCallOption(1, 100)
        
        result = anderson_lake(model, option, self.scheme)
        expected = 4.170956582
    
        self.assertAlmostEqual(result, expected)
    
    def test_itm(self):
        model = HestonModel(121.17361017736597, 0.1197**2, 1.98937, \
                            0.108977**2, 0.33147, -0.5, np.log(1.0005))
        option = EuropeanCallOption(0.50137, 150)
        
        result = anderson_lake(model, option, self.scheme)
        expected = 0.008644233552
        self.assertAlmostEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
