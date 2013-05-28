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

"""
Report.py houses all cases to generate data and graphs used in the report.

To run a report test, add it's function name below the "if __name__ == '__main__':" line.

"""

def STZ_loop():
    """ Show an example of the STZ loop """

    # Set the queue pieces
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

    # Set weights needed to create scenario
    Weightings.height=-1
    Weightings.gaps=10
    Weightings.rows_removed=10

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=5)
    game.status = "report/STZ_loop"
    game.solve()

def LJO_loop():
    """ Show an example of the LJO loop """

    # Set the queue pieces
    pieces = [
        TetrisPiece(5, 1),
        TetrisPiece(4, 2),
        TetrisPiece(2, 3),
        TetrisPiece(5, 4),
        TetrisPiece(4, 5),
        TetrisPiece(2, 6),
    ]

    # Set weights needed to create scenario
    Weightings.height=-3
    Weightings.gaps=10
    Weightings.rows_removed=17

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=5)
    game.status = "report/LJO_loop"
    game.solve()



if __name__ == '__main__':
    STZ_loop()
