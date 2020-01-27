# coding:utf-8
# !/usr/bin/python3

# ------------USE RECOMMENDATIONS-------------
# Default index of the databases passed as argument in the following
# functions is : [Number of seeds eaten by player 1,
#                 Number of seeds eaten by player 2,
#                 Plays (a string of numbers beetween 1 and 6,
#                        representing all the plays made in a game)]
#
# If the index is different, pass the keyword argument columns when using
# the functions (e.g. for a [Nb seeds 2, Random, Plays, Nb seeds 1],
#                you should pass columns=(3, 0, 2)
#
# 'dtb' is used for 'database'
# To follow pandas module choice, the functions return new objects
# rather than modifying them
# --------------------------------------------


import os
import pandas as pd

DTB_PATH = os.path.join('.', 'wari_ludoteka.csv')

# Various functions


def max_series(x, y):
    """
    x, y two pandas.Series objects of same shape, max(x,y) is the
    pandas.Series whose values correspond to the maximum of the
    values of x and y
    """
    return x.combine(y, max).astype(int, errors='ignore')


def min_series(x, y):
    """
    x, y two pandas.Series objects of same shape, min(x,y) is the
    pandas.Series whose values correspond to the minimum of the
    values of x and y
    """
    return x.combine(y, min).astype(int, errors='ignore')


def seeds_number(dtb, round: int, columns=(0, 1, 2)):  # IN WORK
    """
    Display statistics about the round concerned
    round : the round of the game to be studied
    """


def convert_game(game: str):
    """
    game : a string representing a game of Awale, in the same format as
           in the wari_ludoteka base (e.g. 'FaDeFbBc...')
    Return a string representing the same game in numbers format
    (e.g. '5321642...')
    """
    conversion_dict = {'a': 6, 'b': 5, 'c': 4, 'd': 3, 'e': 2, 'f': 1}
    out = ''
    for i in list(game.lower()):
        out += str(conversion_dict[i])
    return out


def convert_games(dtb, columns=(0, 1, 2)):
    """
    Convert all games of dtb (see convert_game)
    """
    col = dtb.columns
    moves = col[columns[2]]  # the name of the moves column

    def convert_column(column):
        return column.apply(convert_game)

    return dtb.apply(lambda column: convert_column(column)
                     if (column.name == moves)
                     else column)


def test_game(plays: str):
    """
    plays : a string representing an Awale game in the number format
           (e.g. '1524634250...', see convert_game function above)
    Return a boolean on whether the game is a real game or not
    (no errors in the plays indicated)
    """
    from src import engine
    from src import player

    plays = [int(i) for i in plays]
    plays0, plays1 = plays[::2], plays[1::2]

    game = engine.Game()
    game.player0, game.player1 = player.Record(
        game, plays0), player.Record(game, plays1)

    try:
        game.run_game()
        return True
    except TypeError:
        return False


def review_game(plays: str):
    """
    plays : a string representing an Awale game in the number format
           (e.g. '1524634250...', see convert_game function above)
    If the game is valid, return the corresponding game stopped when one
    player has eaten more than 24 seeds
    Else return False
    """
    from src import engine
    from src import player
    from numpy import NaN

    playslist = [int(i) for i in plays]
    plays0, plays1 = playslist[::2], playslist[1::2]

    game = engine.Game()
    game.player0, game.player1 = player.Record(
        game, plays0), player.Record(game, plays1)

    try:
        game.run_game()
        surplus = len(game.player0.plays)+len(game.player1.plays)
        if surplus > 0:
            return plays[:-surplus]
        else:
            return plays
    except TypeError:
        return NaN


def review_games(dtb, columns=(0, 1, 2)):
    """Apply review_game on all the database"""
    col = dtb.columns
    moves = col[columns[2]]  # the name of the moves column

    def review_column(column):
        return column.apply(review_game)

    new_dtb = dtb.apply(lambda column: review_column(column)
                        if (column.name == moves)
                        else column)
    return new_dtb.dropna()


def winners_seeds_number(dtb, columns=(0, 1, 2)):
    """
    Return a 49 long list of int, where the (n-1)th number represents the
    number of games won with n seeds eaten by the winner
    """
    from functions import max_series

    col = dtb.columns
    seeds1, seeds2 = dtb[col[columns[0]]], dtb[col[columns[1]]]
    seeds_winner = max_series(seeds1, seeds2)

    seeds_winner = seeds_winner.value_counts()
    # Add zero for each ending number of seeds, to have 49 values
    zeros = pd.Series(49*[0])
    seeds_winner = seeds_winner.add(zeros, fill_value=0).astype(int)

    return list(seeds_winner.sort_index())


def loosers_seeds_number(dtb, columns=(0, 1, 2)):
    """
    Return a 49 long list of int, where the (n-1)th number represents the
    number of games won with n seeds eaten by the looser
    """
    from functions import min_series

    col = dtb.columns
    seeds1, seeds2 = dtb[col[columns[0]]], dtb[col[columns[1]]]
    seeds_looser = min_series(seeds1, seeds2)

    seeds_looser = seeds_looser.value_counts()
    # Add zero for each ending number of seeds, to have 49 values
    zeros = pd.Series(49*[0])
    seeds_looser = seeds_looser.add(zeros, fill_value=0).astype(int)

    return list(seeds_looser.sort_index())


def player_stats(dtb, player1='player1', player2='player2',
                 columns=(0, 1, 2)):
    """
    player1: name of the column containing the id of the 1st player
    Returns a DataFrame mapping each player to the number of games he
    played and the number of wins
    """
    new_dtb = winner(dtb, player1, player2)

    nb_win = new_dtb['winner'].value_counts()
    nb_games1 = new_dtb[player1].value_counts()
    nb_games2 = new_dtb[player2].value_counts()

    nb_games = nb_games1.add(nb_games2, fill_value=0)
    win_rate = nb_win/nb_games

    result = pd.DataFrame({'nb_games': nb_games, 'nb_win': nb_win,
                           'win_rate': win_rate})
    return result.fillna(value=0)

# CHOSEN: 5061
# nb_games    344
# nb_win      336
# win_rate      97.6744
# Name: 4784, dtype: float64

# Functions useful to reformat the database


def nb_moves(dtb, columns=(0, 1, 2)):
    """
    Return a new database with a 'nb of moves played' column added
    """
    col = dtb.columns
    moves = dtb[col[columns[2]]].rename('nb of moves played')

    nb_moves = moves.apply(len)  # count the nb of chars of every value

    return dtb.join(nb_moves)


def players_moves(dtb, columns=(0, 1, 2)):
    """
    Return a new database in which the column 'moves' has been split in
    two columns : 'moves1' and 'moves2', the moves of the first player
    and the moves of the second one
    """
    col = dtb.columns
    moves = dtb[col[columns[2]]]
    moves1_ = moves.apply(lambda game: game[::2])
    moves2_ = moves.apply(lambda game: game[1::2])

    numindex = list(range(len(col)))
    numindex.remove(columns[2])
    new_dtb = dtb.take(numindex, axis=1)
    return new_dtb.assign(moves1=moves1_, moves2=moves2_)


def winner(dtb, player1='player1', player2='player2', columns=(0, 1, 2)):
    """
    player1: the name of the column containing the id of the 1st player
    Returns the database with a 'winner' column added, containing the id
    of the winner for each game
    """
    def game_winner(x, player1, player2, columns):
        col = dtb.columns
        if x[col[columns[0]]] > x[col[columns[1]]]:
            return x[player1]
        else:
            return x[player2]

    winner_column = dtb.apply(lambda x: game_winner(x, player1, player2,
                                                    columns), axis=1)

    return dtb.assign(winner=winner_column)

# Functions to create new interesting database from the first one


def groupby_openings(dtb, length: int, players=0, columns=(0, 1, 2)):  # ON WORK
    """
    Statistics about openings
    length : the lenght of openings considered
    players : if not 0 or False then openings are player specific (see
    the function payers_moves)
    Return a pandas.Groupby object mapping games by their openings
    (e.g. "13254")
    """
    col = dtb.columns
    moves = col[columns[2]]  # Name of the moves column of dtb

    if not(players):
        moves = col[columns[2]]  # Name of the moves column of dtb
        return dtb.groupby(by=lambda x: (dtb[moves][x][0:length]))

    else:
        # Here each game shall contribute twice
        sparsing_dtb = players_moves(dtb, columns)

        max_index = max(dtb.index)
        new_index = [x+max_index for x in dtb.index]

        dtb2 = dtb.copy()
        dtb2.index = new_index
        dtb2 = dtb.append(dtb2)  # dtb with doubled rows

        group = dtb2.groupby(by=lambda x:
                             sparsing_dtb.moves1[x][0:length] if x <= max_index
                             else sparsing_dtb.moves2[x-max_index][0:length])
        return group


def dtb_seeds_winner(dtb, columns=(0, 1, 2)):
    """
    Return a pandas.GroupBy object that gather games which ended with
    the same number of seeds eaten by the winner
    """

    from functions import max_series

    out = dtb.assign(seeds_winner=lambda x: max_series(
        x[x.columns[columns[0]]],
        x[x.columns[columns[1]]]
    ))

    out = out.groupby('seeds_winner')
    return out


def dtb_seeds_looser(dtb, columns=(0, 1, 2)):
    """
    Return a pandas.GroupBy object that gather games which ended with
    the same number of seeds eaten by the looser
    """

    from functions import min_series

    out = dtb.assign(seeds_looser=lambda x: min_series(
        x[x.columns[columns[0]]],
        x[x.columns[columns[1]]]
    ))

    out = out.groupby('seeds_looser')
    return out


def dtb_select_player(dtb, player: int, columns=(0, 1, 2)):
    """
    Returns the database with only the selected player games
    """
    return dtb.query('player1=='+str(player)+' or player2=='+str(player))


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
    dtb = dtb.astype(dtype={
        'player1': int,
        'seeds1': int,
        'player2': int,
        'seeds2': int,
        'moves': str})
    # dtb = dtb.filter(items=[
    #     'seeds1',
    #     'seeds2',
    #     'moves'])  # remove useless columns 'Player 1' and 'Player 2' from dtb
    # convert games representations in numerical
    dtb = convert_games(dtb, (1, 3, 4))

    dtb = dtb.reindex(['seeds1', 'seeds2', 'moves', 'player1',
                       'player2'], axis=1)
    return dtb


dtb = test()

if __name__ == '__main__':

    try:
        dtb = test()
    except FileNotFoundError:
        print('The variable DTB_PATH may be not correct')
