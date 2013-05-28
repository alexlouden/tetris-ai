#-------------------------------------------------------------------------------
# Name:        Tetris Unit Tests
# Purpose:     Unit tests for tetris AI module
#
# Version:     Python 2.7
#
# Author:      Alex Louden, Ruvan Muthu-Krishna
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden & Ruvan Muthu-Krishna 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

from random import randint, choice

import nose
from nose.tools import timed, raises, assert_equals, assert_true, assert_false
from nose.plugins.attrib import attr

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game
from fileops import read_input_file
from shapeops import num_useful_rotations, merge

def test_read_input_file():
    """ Test parsing the given input file matches the expected list """
    actual = read_input_file('exampleinput.txt')
    expected = [1, 2, 3, 4, 5, 2, 7, 1, 6, 1, 4, 3, 2, 1, 5]

    assert_equals(actual, expected)

def test_get_output():
    """ Test TetrisGame.get_output() """
    game = TetrisGame()
    out = game.get_output()
    assert_equals(out, '')

    game.drop(TetrisPiece(1), 2)
    out = game.get_output()
    assert_equals(out, '1 0 2')

    p = TetrisPiece(2)
    p.rotate(3)
    game.drop(p, 4)
    out = game.get_output()
    assert_equals(out, '1 0 2\n2 3 4')


@attr('plots')
def test_plot_shapes():
    """ Test each shape can be plotted (manually verify) """
    # Plot each shape number
    for shape_num in range(1, 8):

        # Square piece
        pieces = [TetrisPiece(shape_num, shape_num)]

        # Game with only one piece
        game = TetrisGame(pieces, 4)
        game.pieces = pieces

        plot_game(game, 'test/plot_shape_{}'.format(shape_num))

@attr('plots')
def test_plot_all_shapes():
    """ Test all shapes can be plotted on the same figure (manually verify) """

    pieces = [TetrisPiece(i, i) for i in range(1, 8)]

    # Game with only one piece (width of 13 fits all 7 standard shapes)
    game = TetrisGame(width=13)
    game.pieces = pieces

    left = 0
    for piece in game.pieces:
        piece.left = left
        left += piece.width

    plot_game(game, 'test/plot_all_shapes')

def test_shape_width_and_heights():
    """ Test shape width and heights match expected """

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
    """ Test moving shapes, polygon coordinates and boundaries """

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
    """ Test rotating shapes, polygon coordinates and boundaries """
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
    """ Test that shapes can't be rotated to invalid rotations """
    # Try to rotate 90 degrees (but rotate only accepts 0,1,2,3)
    p = TetrisPiece(1)
    p.rotate(90)

def test_num_useful_rotations():
    """ Test the number of useful rotations function for each shape """

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
    """ Test merging pieces together """

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
    """ Test calculating the game height """

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

    plot_game(g, 'test/test_game_height')


def test_drop():
    """ Test dropping a piece (manually verify image) """

    g = TetrisGame(width=5)
    g.drop(TetrisPiece(7), 0)
    g.drop(TetrisPiece(1), 0)

    plot_game(g, 'test/test_drop')

    assert_equals(g.height, 6)

    g = TetrisGame(width=5)
    g.drop(TetrisPiece(2), 0)
    g.drop(TetrisPiece(1), 0)
    g.drop(TetrisPiece(1), 1)

    plot_game(g, 'test/test_drop_2')

    assert_equals(g.height, 6)

@raises(ValueError)
def test_drop_out_of_bounds():
    """ Test dropping a piece out of bounds throws an error """

    g = TetrisGame(width=3)
    p = TetrisPiece(1)
    p.rotate(1)
    g.drop(p, 0)


@attr('plots')
def test_random_drop():
    """ Test dropping random pieces (manually verify) """
    # Just for fun

    g = TetrisGame(width=10)

    while g.height < 30:
        piece_id = randint(1, 7)
        left = randint(0, 9)
        rotation = randint(0, 3)
        try:
            g.drop(TetrisPiece(piece_id, rotation=rotation), left)
        except ValueError:
            # Ignore pieces off edge
            pass

    plot_game(g, 'test/test_random_drop')

def test_is_row_full():
    """ Test that full rows have blocks removed """

    g = TetrisGame(width=5)

    g.drop(TetrisPiece(4, 'L', rotation=2), 3)
    g.drop(TetrisPiece(6, 'Z', rotation=1), 1)
    g.drop(TetrisPiece(2, 'square1'), 0)
    g.drop(TetrisPiece(2, 'square2'), 0)

    # Rows 0 and 2 are not full
    assert_false(g.is_row_full(0))
    assert_false(g.is_row_full(2))

    # Row 1 is full
    assert_true(g.is_row_full(1))

    plot_game(g, 'test/test_full_row_0_before')

    assert_equals(g.height, 5)
    num_rows_removed = g.check_full_rows()
    assert_equals(g.height, 4)

    assert_equals(num_rows_removed, 1)

    plot_game(g, 'test/test_full_row_1_after')


def test_check_full_rows():
    """ Test that a single full rows can be removed """

    g = TetrisGame(width=4)
    g.drop(TetrisPiece(1, 'I1', rotation=1), 0)
    g.check_full_rows()

    assert_equals(g.height, 0)

def test_check_full_rows_multiple():
    """ Test that multiple full rows are removed """

    g = TetrisGame(width=4)
    g.drop(TetrisPiece(1, 'I1', rotation=1), 0)
    g.drop(TetrisPiece(1, 'I2', rotation=1), 0)

    plot_game(g, 'test/test_check_full_rows_multiple_0_before')
    num_rows_removed = g.check_full_rows()
    assert_equals(num_rows_removed, 2)
    plot_game(g, 'test/test_check_full_rows_multiple_1_after')

    assert_equals(g.height, 0)

def test_check_full_rows_multiple_2():
    """ Test that full row count works """

    g = TetrisGame(width=5)
    g.drop(TetrisPiece(1, 'I'), 0)
    g.drop(TetrisPiece(2, 'O'), 1)
    g.drop(TetrisPiece(3, 'T'), 3)

    plot_game(g, 'test/test_check_full_rows_multiple_2_0_before')
    num_rows_removed = g.check_full_rows()
    assert_equals(num_rows_removed, 1)
    plot_game(g, 'test/test_check_full_rows_multiple_2_1_after')

    assert_equals(g.height, 3)

def test_check_full_rows_multiple_3():
    """ Test that multiple full row counts works """

    g = TetrisGame(width=4)
    g.drop(TetrisPiece(2), 0)
    g.drop(TetrisPiece(2), 2)

    plot_game(g, 'test/test_check_full_rows_multiple_3_0_before')
    num_rows_removed = g.check_full_rows()
    assert_equals(num_rows_removed, 2)
    plot_game(g, 'test/test_check_full_rows_multiple_3_1_after')

    assert_equals(g.height, 0)

    # Check that calling it again doesn't cause problems
    num_rows_removed = g.check_full_rows()
    assert_equals(num_rows_removed, 0)

def test_check_full_rows_piece_drop():
    """ Check that a floating block does not drop """

    g = TetrisGame(width=4)

    i = TetrisPiece(4, 'Z')
    i.rotate(1)
    g.drop(i, 0)

    i = TetrisPiece(5, 'S')
    i.rotate(3)
    g.drop(i, 1)

    plot_game(g, 'test/test_check_full_rows_piece_drop_0_before')
    num_rows_removed = g.check_full_rows()
    plot_game(g, 'test/test_check_full_rows_piece_drop_1_after')

    assert_equals(num_rows_removed, 1)
    assert_equals(g.height, 2)

    # Check that calling it again doesn't cause problems
    num_rows_removed = g.check_full_rows()
    assert_equals(num_rows_removed, 0)


def test_check_full_rows_plot():
    """ Check that a S piece with the middle missing can be plotted """

    g = TetrisGame(width=6)
    i = TetrisPiece(1, 'I1')
    i.rotate(1)
    g.drop(i, 1)

    i = TetrisPiece(1, 'I2')
    i.rotate(1)
    g.drop(i, 0)

    g.drop(TetrisPiece(6, 'Test'), 4)

    plot_game(g, 'test/test_check_full_rows_plot_0_before')
    num_rows_removed = g.check_full_rows()
    assert_equals(num_rows_removed, 1)
    plot_game(g, 'test/test_check_full_rows_plot_1_after')

    assert_equals(g.height, 2)

    # Check that calling it again doesn't cause problems
    num_rows_removed = g.check_full_rows()
    assert_equals(num_rows_removed, 0)

def test_count_gaps():
    """ Test the count_gaps() function with two squares and an I """
    g = TetrisGame(width=5)

    num_gaps = g.count_gaps()
    assert_equals(num_gaps, 0)

    g.drop(TetrisPiece(2), 0)
    g.drop(TetrisPiece(2), 3)

    num_gaps = g.count_gaps()
    assert_equals(num_gaps, 0)

    g.drop(TetrisPiece(1, rotation=1), 0)

    plot_game(g, 'test/test_count_gaps')

    num_gaps = g.count_gaps()
    assert_equals(num_gaps, 2)

def test_count_gaps_2():
    """ Test the count_gaps() function with two T pieces """

    g = TetrisGame(width=5)

    num_gaps = g.count_gaps()
    assert_equals(num_gaps, 0)

    # Drop a T with no rotation in the middle
    g.drop(TetrisPiece(3, 'T1'), 2)
    num_gaps = g.count_gaps()
    assert_equals(num_gaps, 1)

    plot_game(g, 'test/test_count_gaps_2_1')

    # Drop a T on it's side
    g.drop(TetrisPiece(3, 'T2', 3), 1)
    plot_game(g, 'test/test_count_gaps_2_2')

    num_gaps = g.count_gaps()
    assert_equals(num_gaps, 7)


@attr('plots')
def test_random_drop_gap_count():
    """ Randomly drop pieces until a height of 20 with no gaps """
    # Just for fun

    g = TetrisGame(width=10)

    num_useful = {i: num_useful_rotations(i) for i in range(1, 8)}

    print num_useful

    count = 0
    count_tried = 0

    while g.height < 20:
        piece_id = randint(1, 7)
        left = randint(0, 9)
        rotation = choice(num_useful[piece_id])

        try:
            g.drop(TetrisPiece(piece_id, rotation=rotation), left)
        except ValueError:
            # Ignore pieces off edge
            pass

        num_gaps = g.count_gaps()

        print piece_id, left, rotation, num_gaps, count, g.height

        count_tried += 1

        if num_gaps > 0:
            g.pieces.pop()
        else:
            count += 1

        g.update_merged_pieces()
        g.height = g.calculate_height()

    print count_tried, count
    plot_game(g, 'test/test_random_drop_nogaps')


def test_count_blocks_above_height():
    """ Count the number of blocks (area/centroid) above a given row height 1 """

    g = TetrisGame(width=5)
    g.drop(TetrisPiece(2, 'O'), 1)
    g.drop(TetrisPiece(3, 'T'), 3)

    assert_equals(g.height, 3)
    centroid, area = g.calculate_blocks_above_height(3)
    assert_equals(centroid, 0)
    assert_equals(area, 0)

    # Drop an 1, now one block is above height 3
    g.drop(TetrisPiece(1, 'I'), 0)

    assert_equals(g.height, 4)

    centroid, area = g.calculate_blocks_above_height(3)
    assert_equals(centroid, 0.5)
    assert_equals(area, 1)


def test_count_blocks_above_height_2():
    """ Count the number of blocks (area/centroid) above a given row height 2 """

    # L on it's bottom
    g = TetrisGame(width=7)

    stats = g.calculate_blocks_above_height(0)
    assert_equals(stats, (0,0))

    g.drop(TetrisPiece(5, 'L', 2), 1)

    centroid, area = g.calculate_blocks_above_height(0)
    assert_equals(centroid, 1.25)
    assert_equals(area, 4)

    centroid, area = g.calculate_blocks_above_height(1)
    assert_equals(centroid, 1)
    assert_equals(area, 2)

    plot_game(g, 'test/test_count_blocks_above_height_2')


def test_count_blocks_above_height_3():
    """ Count the number of blocks (area/centroid) above a given row height 3 """

    # L on it's face
    g = TetrisGame(width=7)
    g.drop(TetrisPiece(5, 'L', 1), 1)

    centroid, area = g.calculate_blocks_above_height(0)
    assert_equals(centroid, 1.25)
    assert_equals(area, 4)

    centroid, area = g.calculate_blocks_above_height(1)
    assert_equals(centroid, 0.5)
    assert_equals(area, 3)

    plot_game(g, 'test/test_count_blocks_above_height_3')


if __name__ == '__main__':
    nose.main(argv=['',
        '--verbosity=2',
##        '--with-id',
##        '--failed', # Repeat only previously failed tests
##        '--nocapture', # Don't capture stdout
        '-a !plots', # Ignore tests with 'plots' attribute
        __name__
        ])
