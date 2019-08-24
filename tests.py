#coding:utf-8
#!/usr/bin/python3

# Test script for the database manipulation functions
# To launch the tests, import the script in a Python process, then enter
# "ut.main()" (/!\ That kills the process) 

import pandas as pd
import unittest as ut  # standard test library
from functions import *

class TestDTB(ut.TestCase):
    """
    Class gathering all the tests methods
    """

    def test_max_series(self):
        x, y = pd.Series([9,2,5,4,5,7,2]), pd.Series([1,5,2,63,8,9,2])
        result = max_series(x, y)==pd.Series([9,5,5,63,8,9,2])
        self.assertTrue(result.all())

    def test_convert_game(self):
        game = 'DaCeDfDfAb'
        self.assertEqual(convert_game(game), '3642313165')

    def test_winners_seeds_number(self):
        seeds1 = pd.Series([28,2,13,48,0,19,26,26])
        seeds2 = pd.Series([1,25,24,0,24,5,22,0])
        moves = pd.Series(['','','','','','','',''])

        dtb = pd.DataFrame({'seeds1': seeds1,
                            'seeds2': seeds2,
                            'moves': 'moves'})
        self.assertEqual(winners_seeds_number(dtb),
                         [(24, 2), (25, 1), (26, 2), (27, 0), (28, 1),
                          (29, 0), (30, 0), (31, 0), (32, 0), (33, 0),
                          (34, 0), (35, 0), (36, 0), (37, 0), (38, 0),
                          (39, 0), (40, 0), (41, 0), (42, 0), (43, 0),
                          (44, 0), (45, 0), (46, 0), (47, 0), (48, 1)])

    
        
