#coding:utf-8
#!/usr/bin/python3

import os
import pandas as pd

col = ['Joueur 1', 'Nb graines 1', 'Joueur 2', 'Nb graines 2', 'coups']
bdd_path = os.path.join('.', 'wari_ludoteka.csv')

#Various functions

def max_series(x, y):
        '''x, y two pandas.Series objects of same shape, max(x,y) is the  pandas.Series whose values correspond to the maximum of the values of x and y'''
        return pd.Series([max(x[i], y[i]) for i in range(x.shape[0])], index=x.index)

def nb_de_graines(tour:int, bdd_path, sep=','):
    '''tour : le tour dont on veut avoir les statistiques
    Affiche et retourne le nb de graines dans chaque trou au xième tour'''
    bdd = pd.read_csv(bdd_path, sep=sep)

def convert_game(game:str):
    """game : a string representing a game of Awale, in the same format as in the wari_ludoteka base (e.g. 'FaDeFbBc...')
    Return a string representing the same game in numbers format (e.g. '5321642...')"""
    conversion_dict = {'a':6, 'b':5, 'c':4, 'd':3, 'e':2, 'f':1}
    out = ''
    for i in list(game.lower()):
        out += str(conversion_dict[i])
    return out

def test_game(game:str):
    """game : a string representing an Awale game in the number format (e.g. '1524634250...', see convert_game function above)
    Return a boolean on whether the game is a real game or not (no errors in the plays indicated)"""

    from sys import sys.path
    parent_dir_path = os.path.split(os.getcwd())[0]
    sys.path.append(parent_dir_path)
    import AwAI-dev as awd  #importing this module from the parent directory
    
    game = 1

    sys.path.remove(parent_dir_path) #clearing sys.path

def graines_gagnant(bdd, columns=(col[1],col[3])):
    '''Retourne un  tableau de tuples (n, m), où m est le nombre de parties gagnées avec n graines mangées par le gagnant (columns : liste/tuple des deux colonnes nb graines)'''
    n = bdd.shape[0]
    col = bdd.columns

    nbparties = 50*[0] #nbparties[i] donne le nombre de parties avec i graines managées par le gagnant
    max, graines1, graines2 = 0, 0, 0

    for i in range(n):
        graines1, graines2 = bdd[col[0]][i], bdd[col[1]][i]
        max = (graines1>graines2)*(graines1-graines2) + graines2
        nbparties[max] += 1

    return [(i, nbparties[i]) for i in range(24, 49)]

#Fonctions pour modifier la table

def nb_coups(bdd, sep=','):
    '''Ajoute une colonne "nb de coups joués" à la table'''


# Fonctions pour créer certaines tables intéressantes à partir de l'historique des parties


def bdd_nb_coups(bdd, x:int, sep=','):
    '''Statistics about openings
    x : the lenght of openings to analyze
    Return a pandas.Groupby object mapping games by their openings (e.g. "FaEeBd") to their number of occurences in the database
    if player=1 then the openings will be player specific (e.g. "FaEcDe" contributes for 3-long openings as "FED" and "ace")'''


    


    


def bdd_x_premiers_coups(x:int, bdd, sep=',', player=0):
    '''Return a csv indexed by "x premiers coups", "nb de parties", "parties"
    (gather games that begun with the same x first moves)
    -> if player = 1 or 2 : games where the corresponding player begun
    '''
    try :
        joueur in {0,1,2}
    except ValueError :
        print("joueur doit valoir 1 ou 2 (0 par défaut)")


def bdd_graines_gagnant(bdd):
    '''Return a pandas.GroupBy object that gather games which ended with the same number of seeds eaten by the winner'''
    
    from . import max_series    

    out = bdd.assign(graines_gagnant=lambda x: max_series(x[x.columns[0]], x[x.columns[1]]))

    out = out.groupby('graines_gagnant')
    return out


def test():
    '''useful function for testing : generates a pandas.Dataframe database from wari_ludoteka'''
    
    bdd = pd.read_csv(bdd_path, sep=';')
    bdd = bdd.truncate(before=0, after=108983).rename(columns={'Unnamed: 4':'coups','Nb graines 1':'graines1', 'Nb graines 2':'graines2'})
    bdd = bdd.astype(dtype={'Joueur 1': int, 'graines1': int, 'Joueur 2': int, 'graines2': int, 'coups': str})
    bdd = bdd.filter(items=['graines1','graines2','coups'])  #remove useless columns 'Joueur 1' and 'Joueur 2' from bdd

    
    return bdd

bdd = test()

if __name__ == '__main__':

    bdd = test()
