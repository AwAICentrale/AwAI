#coding:utf-8
#!/usr/bin/python3

#------------USE RECOMMENDATIONS-------------
# Default index of the databases passed as argument in the following
# functions is : [Number of seeds eaten by player 1,
#                 Number of seeds eaten by player 2,
#                 Plays (a string of numbers beetween 1 and 6,
#                        representing all the plays made in a game)]
# If the index is different, pass the keyword argument columns when using
# the functions (e.g. for a [Nb seeds 2, Random, Plays, Nb seeds 1],
#                you should pass columns=(3, 0, 2)
#
# dtb is used for database
#--------------------------------------------


import os
import pandas as pd

DTB_PATH = os.path.join('.', 'wari_ludoteka.csv')

#Various functions

def max_series(x, y):
        """
        x, y two pandas.Series objects of same shape, max(x,y) is the
        pandas.Series whose values correspond to the maximum of the
        values of x and y
        """
        return pd.Series([max(x[i], y[i]) for i in range(x.shape[0])],
                         index=x.index)

def seeds_number(dtb, round: int, columns=(0,1,2)):  # IN WORK
    """
    Display statistics about the round concerned
    round : the round of the game to be studied
    """
    bdd = pd.read_csv(BDD_PATH, sep=sep)

def convert_game(game: str):
    """
    game : a string representing a game of Awale, in the same format as
           in the wari_ludoteka base (e.g. 'FaDeFbBc...')
    Return a string representing the same game in numbers format
    (e.g. '5321642...')
    """
    conversion_dict = {'a':6, 'b':5, 'c':4, 'd':3, 'e':2, 'f':1}
    out = ''
    for i in list(game.lower()):
        out += str(conversion_dict[i])
    return out

def test_game(game: str):  #TO BE REVISED
    """
    game : a string representing an Awale game in the number format
           (e.g. '1524634250...', see convert_game function above)
    Return a boolean on whether the game is a real game or not
    (no errors in the plays indicated)
    """
    from sys import path
    # parent_dir_path = os.path.split(os.getcwd())[0]
    # sys.path.append(parent_dir_path)
    import engine, player  #import this module from the parent directory
    
    game = 1

    sys.path.remove(parent_dir_path) #clearing sys.path

def winners_seeds_number(dtb, columns=(0, 1, 2)): #NEEDS COMMENTS
    """
    Return a list of tuples (n, m), where m is the number of games won
    with n seeds eaten by the the winner
    """
    n = dtb.shape[0]
    col = dtb.columns

    nb_games = 50*[0] #nb_games[i] : number of games won with i seeds
    max, seeds1, seeds2 = 0, 0, 0

    for i in range(n):
        seeds1, seeds2 = dtb[col[columns[0]]][i], dtb[col[columns[1]]][i]
        max = (seeds1>seeds2)*(seeds1-seeds2) + seeds2
        nb_games[max] += 1

    return [(i, nb_games[i]) for i in range(24, 49)]


# Functions useful to reformat the database

def nb_moves(dtb, columns=(0,1,2)):  #ON WORK
    """
    Add a 'nb of moves played' column to the database
    """


# Functions to create new interesting database from the first one

def dtb_nb_moves(dtb, x: int, player=0, columns=(0,1,2)):  #ON WORK
    """
    Statistics about openings
    x : the lenght of openings to analyze
    Return a pandas.Groupby object mapping games by their openings
    (e.g. "FaEeBd") to their number of occurences in the database
    If player=1 then the openings will be player specific
    (e.g. "FaEcDe" contributes for 3-long openings as "FED" and "ace")
    """

def dtb_x_first_moves(x: int, dtb, player=0, columns=(0,1,2)):  #ON WORK
    """Return a csv indexed by "x first moves", "nb of games", "games"
    (gather games that begun with the same x first moves)
    -> if player = 1 or 2 : games where the corresponding player begun
    """
    try :
        player in {0,1,2}
    except ValueError :
        print("player should be 1 or 2 (0 by default)")


def dtb_seeds_winner(dtb, columns=(0,1,2)):
    """
    Return a pandas.GroupBy object that gather games which ended with
    the same number of seeds eaten by the winner
    """
    
    from . import max_series    

    out = dtb.assign(seeds_winner=lambda x: max_series(
                                                x[x.columns[columns[0]]],
                                                x[x.columns[columns[1]]]
                                                 ))

    out = out.groupby('seeds_winner')
    return out

            
# Miscellaneous
            
def test():
    """
    useful function for testing : generates a pandas.Dataframe database
    from wari_ludoteka
    """
    
    dtb = pd.read_csv(DTB_PATH, sep=';')
    dtb = dtb.truncate(before=0, after=108983).rename(columns={
                                                'Unnamed: 4': 'moves',
                                                'Nb graines 1': 'seeds1',
                                                'Nb graines 2': 'seeds2',
                                                'Joueur 1': 'player1',
                                                'Joueur 2': 'player2'})
    print(dtb.columns)
    dtb = dtb.astype(dtype={
                            'player1': int,
                            'seeds1': int,
                            'player2': int,
                            'seeds2': int,
                            'moves': str})
    dtb = dtb.filter(items=[           
                            'seeds1',
                            'seeds2',
                            'moves'])  #remove useless columns 'Player 1'
                                       #and 'Player 2' from dtb
    return dtb

dtb = test()

if __name__ == '__main__':

        try :
            dtb = test()
        except FileNotFoundError :
            print('The variable DTB_PATH may be not correct')
        
