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
from nose.tools import assert_equals, assert_true

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game

"""Game scenario tests to verify correct execution of program modules."""

def test_scenario_1():

    pieces = [
        TetrisPiece(5, 'J'),
        TetrisPiece(4, 'L'),
        TetrisPiece(2, 'O')
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=6)
    game.status = "test_scenario_1"
    game.solve()
    print 'height:', game.height

##    # Check game height is 3
##    assert_equals(game.height, 3)

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
    game.solve()
    print 'height:', game.height

##    # Check game height is 3
##    assert_equals(game.height, 3)


if __name__ == '__main__':
    nose.main(argv=[
        '--verbosity=2',
        '--nocapture', # Don't capture stdout
        __name__
        ])