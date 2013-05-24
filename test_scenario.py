#-------------------------------------------------------------------------------
# Name:        Tetris Scenario Tests
# Purpose:     Scenario tests for tetris AI module
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
from nose.tools import assert_equals, assert_true, assert_less
from nose.plugins.attrib import attr

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game

"""Game scenario tests to verify correct execution of program modules."""

def test_scenario_1():

    pieces = [
        TetrisPiece(5, 'L'),
        TetrisPiece(4, 'J'),
        TetrisPiece(2, 'O'),
        TetrisPiece(1, 'I'),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=6)
    game.status = "test_scenario_1"

    print '-'*80
    print game.status

    game.solve()

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 3
    assert_less(game.height, 3)

def test_scenario_2():

    pieces = [
        TetrisPiece(1, 'I'),
        TetrisPiece(3, 'T'),
        TetrisPiece(6, 'S'),
        TetrisPiece(7, 'Z'),
        TetrisPiece(1, 'I2')
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=6)
    game.status = "test_scenario_2"

    print '-'*80
    print game.status

    game.solve()

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 3
    assert_less(game.height, 3)

@attr('skip')
def test_scenario_3():

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
    game.status = "test_scenario_3"

    print '-'*80
    print game.status

    game.solve()

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 20
##    assert_less(game.height, 20)

if __name__ == '__main__':
    nose.main(argv=[
        '--verbosity=2',
        '--nocapture', # Don't capture stdout
        '-a !skip', # Ignore tests with 'skip' attribute
        __name__
        ])