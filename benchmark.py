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

# Choose higher resolution time counter
time = clock if os.name == 'nt' else time

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game

def main():

##    for num_pieces in range(1, 10):

    print 'num_pieces,time'


    num_pieces = 0
    delay = time_solve(num_pieces)

    print delay

def time_solve(num_pieces):

    start_time = time()

    pieces = [ TetrisPiece(randint(1, 7), i) for i in range(0, 7)]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=7)
    game.status = "benchmark_num_pieces_{}".format(num_pieces)
    game.solve()

    end_time = time()

    return end_time - start_time

if __name__ == '__main__':
    main()
