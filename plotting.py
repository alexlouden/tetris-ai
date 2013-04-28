#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Alex
#
# Created:     28/04/2013
# Copyright:   (c) Alex 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from matplotlib import pyplot
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

SIZE = (8, 10)
shape_edge_colour = '#000000'

def plot_game(game):

    fig = pyplot.figure(1, figsize=SIZE, dpi=90)
    ax = fig.add_subplot(111)

    plot_board(ax, game)
    for piece in game.pieces:
        plot_piece(ax, piece)

    ax.set_title(game.status)

    pyplot.show()

def plot_board(ax, game):
    """Plots the game board"""

    ax.grid(color='k', linestyle=':', linewidth=1)

    height = max(game.height + 5, 10)

    xrange = [0, game.width]
    yrange = [0, height]

    ax.set_xlim(*xrange)
    ax.set_xticks(range(*xrange) + [xrange[-1]])
    ax.set_ylim(*yrange)
    ax.set_yticks(range(*yrange) + [yrange[-1]])
    ax.set_aspect(1)

def plot_piece(ax, piece):
    """Plots a single game piece"""

    colour = piece.colour
    polygon = piece.polygon

    patch = PolygonPatch(polygon, facecolor=colour, edgecolor=shape_edge_colour, alpha=0.5, zorder=2)
    ax.add_patch(patch)


def main():
    from tetris import TetrisGame, TetrisPiece
    from plotting import plot_game

    # Square piece
    pieces = [TetrisPiece(2)]

    # Game with only one piece
    game = TetrisGame(pieces)

    plot_game(game)

if __name__ == "__main__":
    main()
