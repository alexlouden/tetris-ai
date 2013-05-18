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
from nose.tools import timed, raises, assert_equals, assert_true

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game
from fileops import read_input_file
from shapeops import num_useful_rotations, merge

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
    game = TetrisGame(width=13)
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

def test_move():

    p = TetrisPiece(1)

    # Move piece from 0,0 to 1,2
    p.move_to(1, 2)

    # Check properties
    assert_equals(p.left, 1)
    assert_equals(p.bottom, 2)

    # Check polygon
    assert_equals(p.polygon.bounds, (1, 2, 2, 6)) # min_x, min_y, max_x, max_y

    # Move piece from 1,2 to 4,5
    p.move_to(4, 5)
    assert_equals(p.left, 4)
    assert_equals(p.bottom, 5)
    assert_equals(p.polygon.bounds, (4, 5, 5, 9))

    # Move piece with attribute from 4,5 to 4,2
    p.left = 4
    p.bottom = 2

    assert_equals(p.left, 4)
    assert_equals(p.bottom, 2)
    assert_equals(p.polygon.bounds, (4, 2, 5, 6))

def test_rotate():

    # Create a I piece, rotate it 4 times and check bounds
    p = TetrisPiece(1)
    assert_equals(p.rotation, 0)
    assert_equals(p.polygon.bounds, (0, 0, 1, 4))

    p.rotation = 1
    assert_equals(p.rotation, 1)
    assert_equals(p.polygon.bounds, (0, 0, 4, 1))

    p.rotation = 2
    assert_equals(p.rotation, 2)
    assert_equals(p.polygon.bounds, (0, 0, 1, 4))

    p.rotation = 3
    assert_equals(p.rotation, 3)
    assert_equals(p.polygon.bounds, (0, 0, 4, 1))

    p.rotate(0)
    assert_equals(p.rotation, 0)
    assert_equals(p.polygon.bounds, (0, 0, 1, 4))

@raises(ValueError)
def test_invalid_rotation():
    # Try to rotate 90 degrees (but rotate only accepts 0,1,2,3)
    p = TetrisPiece(1)
    p.rotate(90)

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

def test_merge_pieces():

    # Two I shapes next to each other
    p1 = TetrisPiece(1)
    p2 = TetrisPiece(1)
    p2.left = 1

    # Merge pieces into one 2x4 rectangle
    merged = merge([p1, p2])

    assert_equals(merged.bounds, (0, 0, 2, 4))

    # Test geometry relationships
    assert_true(merged.intersects(p1.polygon))
    assert_true(merged.intersects(p2.polygon))
    assert_true(p1.polygon.touches(p2.polygon))

def test_calculate_height():

    # Create game with an I and a square with one gap
    p1 = TetrisPiece(2)
    p2 = TetrisPiece(1)
    p2.left = 3

    g = TetrisGame()
    g.pieces = [p1, p2]
    g.update_merged_pieces()

    # Height should be 4
    assert_equals(g.calculate_height(), 4)

    # Add two more squares on top of piece 2
    p3 = TetrisPiece(2)
    p3.bottom = 2
    p4 = TetrisPiece(2)
    p4.bottom = 4

    g.pieces = [p1, p2, p3, p4]
    g.update_merged_pieces()

    assert_equals(g.calculate_height(), 6)

    plot_game(g, 'test_game_height')


def test_drop():

    g = TetrisGame(width=5)
    g.drop(TetrisPiece(7), 0)
    g.drop(TetrisPiece(1), 0)

    plot_game(g, 'test_drop')

    assert_equals(g.height, 6)

    g = TetrisGame(width=5)
    g.drop(TetrisPiece(2), 0)
    g.drop(TetrisPiece(1), 0)
    g.drop(TetrisPiece(1), 1)

    plot_game(g, 'test_drop_2')

    assert_equals(g.height, 4)


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
