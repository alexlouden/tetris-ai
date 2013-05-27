#-------------------------------------------------------------------------------
# Name:        Report.py
# Purpose:     Hold all scenarios needed for the report
#
# Version:     Python 2.7
#
# Author:      Alex Louden, Ruvan Muthu-Krishna
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden & Ruvan Muthu-Krishna 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

import os
from pprint import pprint

from tetris import TetrisGame, TetrisPiece
from plotting import plot_game
from ai import Weightings

def STZ_loop():

    pieces = [
        TetrisPiece(3, 1),
        TetrisPiece(6, 2),
        TetrisPiece(7, 3),
        TetrisPiece(6, 4),
        TetrisPiece(7, 5),
        TetrisPiece(3, 6),
        TetrisPiece(3, 7),
        TetrisPiece(7, 8),
        TetrisPiece(6, 9),
        TetrisPiece(7, 10),
        TetrisPiece(6, 11),
        TetrisPiece(3, 13),
    ]

    Weightings.height=-1
    Weightings.gaps=10
    Weightings.rows_removed=10

    game = TetrisGame(pieces, width=5)
    game.status = "report/STZ_loop"
    game.solve()

def LJO_loop():

    pieces = [
        TetrisPiece(5, 1),
        TetrisPiece(4, 2),
        TetrisPiece(2, 3),
        TetrisPiece(5, 4),
        TetrisPiece(4, 5),
        TetrisPiece(2, 6),
    ]

    Weightings.height=-3
    Weightings.gaps=10
    Weightings.rows_removed=17

    game = TetrisGame(pieces, width=5)
    game.status = "report/LJO_loop"
    game.solve()

def plot_cost():
    """ Show simple T -- on side with gap under it,  and on its back - no gap. """

    game = TetrisGame(width=4)
    game.drop(TetrisPiece(3), 0)

    from plotting import plot_piece, plot_board, pyplot

    fig = pyplot.gcf()
    fig.set_size_inches(6, 4)

    # Plot T on side
    ax = fig.add_subplot(121)
    plot_board(ax, game, 5)
    for piece in game.pieces:
        plot_piece(ax, piece)
        ax.plot(piece.polygon.centroid.x, piece.polygon.centroid.y, 'x')
    ax.set_title("T shape")

    # Show gap under T
    import matplotlib.patches as patches
    ax.add_patch(patches.Rectangle((1.1,0.1), 0.8, 0.8, color='r', alpha=0.4))
    ax.text(1.5, 0.5, 'Gap',
        horizontalalignment='center',
        verticalalignment='center')

    # Rotate T
    game.pieces[0].rotate(1)
    ax = fig.add_subplot(122)
    plot_board(ax, game, 5)
    for piece in game.pieces:
        plot_piece(ax, piece)
        ax.plot(piece.polygon.centroid.x, piece.polygon.centroid.y, 'x')
    ax.set_title("Rotated T shape")

##    pyplot.show()
    pyplot.savefig('report/T_gap.png', dpi=100)


if __name__ == '__main__':
    plot_cost()
