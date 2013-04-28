#-------------------------------------------------------------------------------
# Name:        Tetris Unit Tests
# Purpose:     Unit tests for tetris AI module
#
# Version:     Python 2.7
#
# Author:      Alex Louden
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

import nose
from nose.tools import timed, raises, assert_equals

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game
from fileops import read_input_file

def test_read_input_file():
    actual = read_input_file('exampleinput.txt')
    expected = [1, 2, 3, 4, 5, 2, 7, 1, 6, 1, 4, 3, 2, 1, 5]

    assert_equals(actual, expected)

def test_write_output_file():
    pass

def test_plot_shapes():

    # Plot each shape number
    for shape_num in range(1, 8):

        # Square piece
        pieces = [TetrisPiece(shape_num, shape_num)]

        # Game with only one piece
        game = TetrisGame(pieces)
        game.pieces = pieces

        plot_game(game, 'test_shape_{}'.format(shape_num))

def test_plot_two_shapes():
    # Square piece
    pieces = [TetrisPiece(1, 'one'), TetrisPiece(2, 'two')]

    # Game with only one piece
    game = TetrisGame(pieces)
    game.pieces = pieces

    plot_game(game, 'test_two_shapes')

if __name__ == '__main__':
    nose.main(argv=[
        '--failed',
        '--verbosity=2',
        '--nocapture'
        ])
