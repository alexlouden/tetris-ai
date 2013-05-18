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

def test_move_piece():

    p = TetrisPiece(1)

    # Move piece from 0,0 to 1,2
    p.move_to(1, 2)

    # Check properties
    assert_equals(p.left, 1)
    assert_equals(p.bottom, 2)

    # Check polygon
    assert_equals(p.polygon.bounds, (1, 2, 2, 6)) # min_x, min_y, max_x, max_y

    # Move piece from 1,2 to 5,6
    p.move_to(4, 5)
    assert_equals(p.left, 4)
    assert_equals(p.bottom, 5)
    assert_equals(p.polygon.bounds, (4, 5, 5, 9))

    # Move piece with attribute
    p.left = 4
    p.bottom = 2

    assert_equals(p.left, 4)
    assert_equals(p.bottom, 2)
    assert_equals(p.polygon.bounds, (4, 2, 5, 6))

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

    piece_l = TetrisPiece(4, 'L')
    piece_j = TetrisPiece(5, 'J')
    piece_o = TetrisPiece(2, 'O')

    piece_j.left = 2
    piece_o.left = 1

    pieces = [piece_l, piece_j, piece_o]

    # Initialise game with list of pieces
    game = TetrisGame(width=4)
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
