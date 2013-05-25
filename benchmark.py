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

def main():

    # 10 random sets of pieces
    for i in range(10):

        pieces = [ TetrisPiece(randint(1, 7), i) for i in range(0, 7)]
        pprint(pieces)

        piece_delays = []

        for num_pieces in range(1, len(pieces)):
            delay = time_solve(deepcopy(pieces[:num_pieces]), num_pieces)
            piece_delays.append((num_pieces, delay))

        print '-'*40
        print 'num_pieces time'
        pprint(piece_delays)

def time_solve(pieces, num_pieces):

    start_time = time()

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=7)
    game.status = "benchmark_num_pieces_{}".format(num_pieces)
    game.solve()

    end_time = time()
    return end_time - start_time

if __name__ == '__main__':
    main()
