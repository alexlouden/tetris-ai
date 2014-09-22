#-------------------------------------------------------------------------
# Name:        Tetris Scenario Tests
# Purpose:     Scenario tests for tetris AI module
#
# Version:     Python 2.7
#
# Author:      Alex Louden, Ruvan Muthu-Krishna
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden & Ruvan Muthu-Krishna 2013
# Licence:     MIT
#-------------------------------------------------------------------------

import nose
from nose.tools import assert_equals, assert_true, assert_less
from pprint import pprint
from random import shuffle

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game
from shapeops import Pieces

"""
Game scenario tests to verify correct execution of program modules.
Also used to ensure that the AI module doesn't regress, by including a
minimum game height at the end of each scenario.

Have included some scenarios with diagonal edges, to demonstrate the program's
full capabilities.

To skip a scenario add "@attr('skip')" above its definition

"""

# @attr('skip')


def test_scenario_1():

    # Set the queue pieces
    pieces = [
        TetrisPiece(5, 'L'),
        TetrisPiece(4, 'J'),
        TetrisPiece(2, 'O'),
        TetrisPiece(1, 'I'),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=6)
    game.status = "scenario/scenario_1"

    print '-' * 80
    print game.status

    game.solve()

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is equal to 1
    assert_equals(game.height, 1)


# @attr('skip')
def test_scenario_2():

    # Set the queue pieces
    pieces = [
        TetrisPiece(1, 'I'),
        TetrisPiece(3, 'T'),
        TetrisPiece(6, 'S'),
        TetrisPiece(7, 'Z'),
        TetrisPiece(1, 'I2')
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=6)
    game.status = "scenario/scenario_2"

    print '-' * 80
    print game.status

    game.solve()

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 3
    assert_less(game.height, 3)


# @attr('skip')
def test_scenario_3():

    # Set the queue pieces
    pieces = [
        TetrisPiece(3, 'T1'),
        TetrisPiece(6, 'S1'),
        TetrisPiece(7, 'Z1'),
        TetrisPiece(6, 'S2'),
        TetrisPiece(7, 'Z2'),

        TetrisPiece(3, 'T2'),
        TetrisPiece(6, 'S3'),
        TetrisPiece(7, 'Z3'),
        TetrisPiece(6, 'S4'),
        TetrisPiece(7, 'Z4'),

        TetrisPiece(3, 'T3'),
        TetrisPiece(6, 'S5'),
        TetrisPiece(7, 'Z5'),
        TetrisPiece(6, 'S6'),
        TetrisPiece(7, 'Z7'),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=10)
    game.status = "scenario/scenario_3_threaded"

    print '-' * 80
    print game.status

    game.solve()

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 10
    assert_less(game.height, 12)


# @attr('skip')
def test_scenario_4():

    # Set the queue pieces
    pieces = [
        TetrisPiece(1, 'I1'),
        TetrisPiece(4, 'J'),
        TetrisPiece(1, 'I2'),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=5)

    game.drop(TetrisPiece(4, 'J'), 0)
    game.drop(TetrisPiece(7, 'Z'), 3)

    game.status = "scenario/scenario_4"

    print '-' * 80
    print game.status

    game.solve()

    pprint(game.moves)

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 3
    assert_less(game.height, 5)


# @attr('skip')
def test_scenario_5():

    # Set the queue pieces
    pieces = [
        TetrisPiece(2, '[]'),
        TetrisPiece(1, 'I1'),
        TetrisPiece(1, 'I2'),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=5)

    l = TetrisPiece(5, 'L')
    l.rotate(2)
    game.drop(l, 0)

    j = TetrisPiece(4, 'J')
    j.rotate(2)
    game.drop(j, 2)

    game.status = "scenario/scenario_5"

    print '-' * 80
    print game.status

    game.solve()

    pprint(game.moves)

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is zero
    assert_equals(game.height, 0)


# @attr('skip')
def test_scenario_6():

    # Set the queue pieces
    pieces = [
        TetrisPiece(2, '[]'),
        TetrisPiece(1, 'I1'),
        TetrisPiece(1, 'I2'),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=6)

    l = TetrisPiece(5, 'L')
    l.rotate(2)
    game.drop(l, 0)

    j = TetrisPiece(4, 'J')
    j.rotate(2)
    game.drop(j, 2)

    game.status = "scenario/scenario_6"
    game.solve()

    pprint(game.moves)

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is equal to 1
    assert_equals(game.height, 1)

##    for move in game.moves:
##        print move.stats

    # Check that the two Is are on the right:
    assert_equals(game.pieces[0].left, 4)
    assert_equals(game.pieces[1].left, 5)
    assert_equals(game.pieces[1].polygon.bounds, (5, 0, 6, 1))


# @attr('skip')
def test_scenario_7():

    # Set the queue pieces
    pieces = [
        TetrisPiece(3, 'T'),
        TetrisPiece(7, 'Z1'),
        TetrisPiece(7, 'Z2'),
        TetrisPiece(7, 'Z3'),
        TetrisPiece(7, 'Z4'),
        TetrisPiece(7, 'Z5'),
        TetrisPiece(7, 'Z6'),
        TetrisPiece(6, 'S'),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=14)
    game.status = "scenario/scenario_7"
    game.solve()

    pprint(game.moves)

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 3
    assert_less(game.height, 3)


# @attr('skip')
def test_scenario_8():

    # Plus shape
    Pieces.piece_shapes[8] = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (
        2, 2), (3, 2), (3, 1), (2, 1), (2, 0), (1, 0), (1, 1), (0, 1)]
    Pieces.piece_colours[8] = '#AAAAAA'

    # Space ship shape
    Pieces.piece_shapes[9] = [(0, 1), (0, 2), (1, 3), (2, 3), (
        3, 2), (2, 2), (2, 1), (3, 1), (2, 0), (1, 0), (0, 1)]
    Pieces.piece_colours[9] = '#9000ff'

    # Set the queue pieces
    pieces = [TetrisPiece(i, i) for i in range(1, 10)]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=11)
    game.status = "scenario/scenario_8"
    game.solve()

    pprint(game.moves)

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 3
    assert_less(game.height, 6)


# @attr('skip')
def test_scenario_9():

    # Plus shape
    Pieces.piece_shapes[8] = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (
        2, 2), (3, 2), (3, 1), (2, 1), (2, 0), (1, 0), (1, 1), (0, 1)]
    Pieces.piece_colours[8] = '#AAAAAA'

    # Space ship shape
    Pieces.piece_shapes[9] = [(0, 1), (0, 2), (1, 3), (2, 3), (
        3, 2), (2, 2), (2, 1), (3, 1), (2, 0), (1, 0), (0, 1)]
    Pieces.piece_colours[9] = '#9000ff'

    # Set the queue pieces
    pieces = [
        TetrisPiece(8, 1),
        TetrisPiece(9, 2),
        TetrisPiece(8, 3),
        TetrisPiece(9, 4),
        TetrisPiece(8, 5),
        TetrisPiece(9, 6),
        TetrisPiece(8, 7),
        TetrisPiece(9, 8),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=7)
    game.status = "scenario/scenario_9"
    game.solve()

    pprint(game.moves)

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is equal to 10
    assert_equals(game.height, 10)


# @attr('skip')
def test_diagonal_shapes():
    """ Crazy diagonal shapes """

    # Set the queue pieces
    Pieces.piece_shapes = {
        1: [(0, 1), (1, 0), (1, 3), (0, 4), (0, 1)],
        2: [(0, 1), (1, 0), (2, 1), (1, 2), (0, 1)],
        3: [(1, 0), (0, 1), (0, 2), (1, 3), (1, 2), (2, 2), (2, 1), (1, 1), (1, 0)],
        4: [(0, 0), (0, 3), (1, 3), (2, 2), (1, 2), (1, 1)],
        5: [(0, 2), (1, 3), (2, 2), (2, 0), (1, 0), (1, 2), (0, 2)],
        6: [(0, 1), (0, 3), (1, 2), (2, 2), (2, 0), (1, 1), (0, 1)],
        7: [(0, 1), (0, 2), (1, 2), (1, 3), (2, 2), (2, 1), (1, 1), (1, 0), (0, 1)],
    }

    pieces = [TetrisPiece(i, i) for i in sorted(Pieces.piece_shapes.keys())]
    shuffle(pieces)

    # Initialise empty game
    game = TetrisGame(width=13)

    left = 0
    for piece in pieces:
        game.drop(piece, left)
        left += piece.width

    game.status = "scenario/diagonal_shapes"
    plot_game(game, 'test/plot_diagonal_shapes')

    # Random 4 buckets
    pieces = [TetrisPiece(shapenum, id)
              for id, shapenum in enumerate(Pieces.piece_shapes.keys() * 3)]
    shuffle(pieces)

    pprint(pieces)

    game = TetrisGame(pieces, width=5)
    game.status = "scenario/diagonal_shapes_shuffle"
    game.solve()

# @attr('skip')


def test_scenario_10():
    """ Tessellating Houses """

    # Set the queue pieces
    Pieces.piece_shapes = {
        1: [(0, 0), (2, 0), (2, 1), (1, 2), (0, 1)],
    }

    pieces = [TetrisPiece(1, id) for id in range(10)]

    game = TetrisGame(pieces, width=6)
    game.status = "scenario/scenario_10"
    game.solve()

    pprint(game.moves)
    print game.height


if __name__ == '__main__':

##    # Do time profile
##    import cProfile
##    cProfile.run('test_scenario_3()')

    nose.main(argv=[
        '',
        '--verbosity=2',
        '--nocapture',  # Don't capture stdout
        '-a !skip',  # Ignore tests with 'skip' attribute
        __name__
    ])
