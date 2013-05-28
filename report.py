#-------------------------------------------------------------------------------
# Name:        Report.py
# Purpose:     Hold all scenarios needed for the report
#
# Version:     Python 2.7
#
# Author:      Alex Louden, Ruvan Muthu-Krishna
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden & Ruvan Muthu-Krishna 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

import os
from time import clock, time
from random import randint
from copy import deepcopy
from pprint import pprint

# Choose higher resolution time counter
time = clock if os.name == 'nt' else time

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game
from ai import Weightings

def STZ_loop():

    pieces = [
        TetrisPiece(3, 1),
        TetrisPiece(6, 2),
        TetrisPiece(7, 3),
        TetrisPiece(6, 4),
        TetrisPiece(7, 5),
        TetrisPiece(3, 6),
        TetrisPiece(3, 7),
        TetrisPiece(7, 8),
        TetrisPiece(6, 9),
        TetrisPiece(7, 10),
        TetrisPiece(6, 11),
        TetrisPiece(3, 13),
    ]

    Weightings.height=-1
    Weightings.gaps=10
    Weightings.rows_removed=10

    game = TetrisGame(pieces, width=5)
    game.status = "report/STZ_loop"
    game.solve()

def LJO_loop():

    pieces = [
        TetrisPiece(5, 1),
        TetrisPiece(4, 2),
        TetrisPiece(2, 3),
        TetrisPiece(5, 4),
        TetrisPiece(4, 5),
        TetrisPiece(2, 6),
    ]

    Weightings.height=-3
    Weightings.gaps=10
    Weightings.rows_removed=17

    game = TetrisGame(pieces, width=5)
    game.status = "report/LJO_loop"
    game.solve()

def test_rows_score():

    num_pieces = 20

    pieces = [ TetrisPiece(randint(1, 7), i) for i in range(0, num_pieces)]
    pprint(pieces)

    # Try -1 to -10
    for rr in (1, 5, 10):
        Weightings.rows_removed = rr

        game = TetrisGame(deepcopy(pieces), width=7)
        game.status = "report/rows_removed_{}".format(Weightings.rows_removed)
        game.solve()

        print Weightings.rows_removed, game.height


if __name__ == '__main__':
    test_rows_score()
