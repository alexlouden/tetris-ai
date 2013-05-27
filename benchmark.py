#-------------------------------------------------------------------------------
# Name:        Tetris Benchmarking
# Purpose:     Benchmarking functions
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


def test_gaps_score():
    """ Vary gaps parameters and record game.height """

    num_pieces = 20

    Weightings.lookahead_distance = 4
    Weightings.starting_score = 100

    pieces = [ TetrisPiece(randint(1, 7), i) for i in range(0, num_pieces)]
    pprint(pieces)

    # Try 1 to 10
    for g in range(1, 11):
        Weightings.gaps = g

        game = TetrisGame(deepcopy(pieces), width=7)
        game.status = "benchmark/gaps_{}".format(Weightings.gaps)
        game.solve()

        print Weightings.gaps, game.height


def test_rows_score():
    """ Vary rows_removed parameters and record game.height """

    num_pieces = 20

    Weightings.lookahead_distance = 3
    Weightings.max_num_branches = 3
    Weightings.starting_score = 100

    pieces = [ TetrisPiece(randint(1, 7), i) for i in range(0, num_pieces+1)]
    pprint(pieces)

    # Try -1 to -10
    for rr in range(-1, -11, -1):
        Weightings.rows_removed = rr

        game = TetrisGame(deepcopy(pieces), width=7)
        game.status = "benchmark/rows_removed_{}".format(Weightings.rows_removed)
        game.solve()

        print Weightings.rows_removed, game.height


def benchmark_time_vs_height():

    num_pieces = 10
    num_sets = 50

    print 'i branches lookahead delay height'

    # A random sets of pieces
    for i in range(num_sets):

        # 50 random pieces from 1-7
        pieces = [ TetrisPiece(randint(1, 7), piece_id) for piece_id in range(0, num_pieces)]

        for branches in [3, 2, 1]:
            Weightings.max_num_branches = branches

            for lookahead in [3, 2, 1]:
                Weightings.lookahead_distance = lookahead

                name = 'benchmark/set_{}_b{}_l{}'.format(i, branches, lookahead)
                delay, height, game = time_solve(deepcopy(pieces), name)
                plot_game(game, name)

                print i, branches, lookahead, delay, height


def time_solve(pieces, name):

    start_time = time()

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=7)
    game.status = name
    game.solve()

    end_time = time()
    delay = end_time - start_time
    return delay, game.height, game

if __name__ == '__main__':
    benchmark_time_vs_height()
