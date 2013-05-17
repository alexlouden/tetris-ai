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
from shapeops import num_useful_rotations

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
        game = TetrisGame(pieces, 4)
        game.pieces = pieces

        plot_game(game, 'test_shape_{}'.format(shape_num))

def test_plot_all_shapes():
    pieces = [TetrisPiece(i, i) for i in range(1, 8)]

    # Game with only one piece (width of 13 fits all 7 standard shapes)
    game = TetrisGame(pieces, 13)
    game.pieces = pieces

    left = 0
    for piece in game.pieces:
        piece.left = left
        left += piece.width

    plot_game(game, 'test_all_shapes')

def test_shape_width_and_heights():

    # Shapes 2-7 have width of 2
    expected_widths = {i: 2 for i in range(2,8)}
    # Shape 1 has 1 width
    expected_widths[1] = 1

    # Shapes 3-7 have height of 3
    expected_heights = {i: 3 for i in range(3,8)}
    # Shape 1 has 4 height
    expected_heights[1] = 4
    # Shape 2 has 2 height
    expected_heights[2] = 2

##    print expected_widths, expected_heights

    pieces = [TetrisPiece(i) for i in range(1, 8)]
    for piece in pieces:
        assert_equals(piece.width, expected_widths[piece.num])
        assert_equals(piece.height, expected_heights[piece.num])

def test_num_useful_rotations():

    expected_useful_rotations = {
        1: [0, 1],
        2: [0],
        3: [0, 1, 2, 3],
        4: [0, 1, 2, 3],
        5: [0, 1, 2, 3],
        6: [0, 1],
        7: [0, 1]
    }

    for i in range(1, 8):
        assert_equals(num_useful_rotations(i), expected_useful_rotations[i])


def test_scenarios():

    piece_t = TetrisPiece(3, 'T')
    piece_steve = TetrisPiece(4, 'Steve')

    piece_steve.bottom = 5

    pieces = [piece_t, piece_steve]

    # Initialise game with list of pieces
    game = TetrisGame()
    game.pieces = pieces
    game.status = "Scenario 1"

##    game.calculate_height()

    plot_game(game, 'test_scenario')

if __name__ == '__main__':
    nose.main(argv=[
        '--failed',
        '--verbosity=2',
        '--nocapture'
        ])
