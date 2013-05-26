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
from pprint import pprint

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game

"""Game scenario tests to verify correct execution of program modules."""

@attr('skip')
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

@attr('skip')
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

    # Check game height is less than 10
    assert_less(game.height, 12)

@attr('skip')
def test_scenario_4():

    pieces = [
        TetrisPiece(1, 'I1'),
        TetrisPiece(4, 'J'),
        TetrisPiece(1, 'I2'),
    ]

    # Initialise game with list of pieces
    game = TetrisGame(pieces, width=5)

    game.drop(TetrisPiece(4, 'J'), 0)
    game.drop(TetrisPiece(7, 'Z'), 3)

    game.status = "test_scenario_4"

    print '-'*80
    print game.status

    game.solve()

    pprint(game.moves)

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 3
    assert_less(game.height, 5)

@attr('skip')
def test_scenario_5():

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

    game.status = "test_scenario_5"

    print '-'*80
    print game.status

    game.solve()

    pprint(game.moves)

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is zero
    assert_equals(game.height, 0)

def test_scenario_6():

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

    game.status = "test_scenario_6"

    print '-'*80
    print game.status

    game.solve()

    pprint(game.moves)

    # Check positioning of piece 1 - square

    print game.moves[-1].game.pieces

##    self.game.pieces[-1].bottom
##1
##[Dbg]>>> self.game.pieces[-1].left
##1
##[Dbg]>>> self.game.pieces[-1].polygon
##<shapely.geometry.polygon.Polygon object at 0x03249C70>
##[Dbg]>>> self.game.pieces[-1].polygon.bounds
##(1.0, 1.0, 3.0, 3.0)
##[Dbg]>>> self.game.pieces[3].polygon.bounds
##Traceback (most recent call last):
##  File "<interactive input>", line 1, in <module>
##IndexError: list index out of range
##[Dbg]>>> self.game.pieces[2].polygon.bounds
##(1.0, 1.0, 3.0, 3.0)

    for move in game.moves:
        print move.stats

    # Check that there were moves for each piece
    assert_equals(len(game.moves), len(pieces))

    # Check game height is less than 3
    assert_less(game.height, 5)

if __name__ == '__main__':

    # Do time profile?
##    import cProfile
##    cProfile.run('test_scenario_2()')

    nose.main(argv=[
        '--verbosity=2',
        '--nocapture', # Don't capture stdout
        '-a !skip', # Ignore tests with 'skip' attribute
        __name__
        ])