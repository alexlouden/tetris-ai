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
from nose.tools import timed, raises, assert_equals, assert_true
from nose.plugins.attrib import attr

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game
from fileops import read_input_file
from shapeops import num_useful_rotations, merge

def test_scenario_1():
    piece_l = TetrisPiece(4, 'L')
    piece_j = TetrisPiece(5, 'J')
    piece_o = TetrisPiece(2, 'O')

    # Initialise game with list of pieces
    game = TetrisGame(width=4)

    game.drop(piece_o, 1)
    game.drop(piece_l, 0)
    game.drop(piece_j, 2)

    game.status = "Scenario 1"

    # Check game height is 3
    assert_equals(game.height, 3)

    plot_game(game, 'test_scenario_1')





if __name__ == '__main__':
    nose.main(argv=[
        '--verbosity=2',
        '--nocapture', # Don't capture stdout
        __name__
        ])