#coding:utf-8
#!/usr/bin/python3

# Test script for the database manipulation functions
# To launch the tests, import the script in a Python process, then enter
# "ut.main()" (/!\ That kills the process) 
#
# At the end is defined DTB_TEST, a sample of the wari_ludoteka database,
# used in some of the testing functions (and COLUMNS_TEST)

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
        self.assertEqual(winners_seeds_number(DTB_TEST, COLUMNS_TEST),
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 4, 1, 1, 2, 1,
                          0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                          0])

    def test_nb_moves(self):
        expected = pd.Series([177, 52, 79, 45, 110, 69, 168, 66, 102,
                              125, 99, 116, 62, 128, 66, 129, 37, 43,
                              39, 111],
                             index=[63065, 30459, 41286, 57839, 1399,
                                    100033, 2464, 78086, 2596, 50564,
                                    89719, 170, 107040, 98170, 17881,
                                    7245, 930, 96587, 108850, 4791])
        expected = expected.rename('nb of moves played')
        result = (nb_moves(DTB_TEST, COLUMNS_TEST)['nb of moves played']
                                                               ==expected)
        self.assertTrue(result.all())
    
    def test_grouby_openings(self):
        from pandas import Int64Index
        expected = Int64Index([7245, 4791, 109780], dtype='int64')
        result = groupby_openings(DTB_TEST, 3, players=1,
                                  columns=COLUMNS_TEST)
        self.assertEqual(result.groups['636'], expected)


DTB_TEST = pd.read_csv(DTB_PATH, sep=';')
random_rows = [63065, 30459, 41286, 57839, 1399, 100033, 2464, 78086,
               2596, 50564, 89719, 170, 107040, 98170, 17881, 7245,
               930, 96587, 108850, 4791] # 20 random games, as a sample
DTB_TEST = DTB_TEST.take(random_rows).rename(columns={
                                                'Unnamed: 4': 'moves',
                                                'Nb graines 1': 'seeds1',
                                                'Nb graines 2': 'seeds2',
                                                'Joueur 1': 'player1',
                                                'Joueur 2': 'player2'})
DTB_TEST = DTB_TEST.astype(dtype={
                        'player1': int,
                        'seeds1': int,
                        'player2': int,
                        'seeds2': int,
                        'moves': str})
DTB_TEST = DTB_TEST.reindex(['moves','seeds2','player2','player1','seeds1'], axis='columns')
COLUMNS_TEST = (4, 1, 0)
DTB_TEST = convert_games(DTB_TEST, COLUMNS_TEST)


