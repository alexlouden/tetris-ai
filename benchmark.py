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

    num_pieces = 20

    Weightings.lookahead_distance = 4
    Weightings.starting_score = 100

    pieces = [ TetrisPiece(randint(1, 7), i) for i in range(0, num_pieces)]
    pprint(pieces)

    # Try 1 to 10
    for g in range(1, 11):
        Weightings.gaps = g

        game = TetrisGame(deepcopy(pieces), width=7)
        game.status = "benchmark_gaps_{}".format(Weightings.gaps)
        game.solve()

        print Weightings.rows_removed, game.height


def test_rows_score():

    num_pieces = 20

    Weightings.lookahead_distance = 4
    Weightings.starting_score = 100

    pieces = [ TetrisPiece(randint(1, 7), i) for i in range(0, num_pieces)]
    pprint(pieces)

    # Try -1 to -10
    for rr in range(-1, -11, -1):
        Weightings.rows_removed = rr

        game = TetrisGame(deepcopy(pieces), width=7)
        game.status = "benchmark_rows_removed_{}".format(Weightings.rows_removed)
        game.solve()

        print Weightings.rows_removed, game.height


def benchmark_time_vs_num_pieces():

    Weightings.lookahead_distance = 4

    # 10 random sets of pieces
    for i in range(10):

        pieces = [ TetrisPiece(randint(1, 7), i) for i in range(0, 7)]
        pprint(pieces)

        piece_delays = []

        for num_pieces in range(1, len(pieces)+1):
            delay = time_solve(deepcopy(pieces[:num_pieces]), num_pieces)
            piece_delays.append((num_pieces, delay))

        print '-'*40
        print 'num_pieces time'
        pprint(piece_delays)
        print '-'*40

def time_solve(pieces, num_pieces):

    start_time = time()

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=7)
    game.status = "benchmark_num_pieces_{}".format(num_pieces)
    game.solve()

    end_time = time()
    return end_time - start_time

if __name__ == '__main__':
    test_gaps_score()
    test_rows_score()

