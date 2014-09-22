#-------------------------------------------------------------------------
# Name:        Plotting Functions
# Purpose:     Functions to plot the game and pieces
#
# Version:     Python 2.7
#
# Author:      Alex Louden
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden 2013
# Licence:     MIT
#-------------------------------------------------------------------------

from matplotlib import pyplot
from descartes.patch import PolygonPatch

shape_edge_colour = '#000000'
shape_alpha = 0.8
id_font_size = 10


def plot_game(game, filename=None):
    """Plots the tetris game.

    Plot to file if a filename is given, otherwise plot to the screen.
    """

    board_height = int(max(game.height + 2, 8))

    # Create figure and resize
    pyplot.clf()
    fig = pyplot.gcf()
    fig.set_size_inches(8, board_height * 0.5 + 1)

    ax = fig.add_subplot(111)

    # Plot the board and pieces
    plot_board(ax, game, board_height)
    for piece in game.pieces:
        plot_piece(ax, piece)

    # Add the game title
    ax.set_title(game.status)

    # Plot to file or screen
    if filename is None:
        # Show the plot
        pyplot.show()
    else:
        # Otherwise, save as PNG
        if not filename.lower().endswith('.png'):
            filename += '.png'

        pyplot.savefig(filename, dpi=120)


def plot_board(ax, game, height):
    """Helper - Plots the game board"""

    ax.grid(color='k', linestyle=':', linewidth=1)

    xrange = [0, game.width]
    yrange = [0, height]

    ax.set_xlim(*xrange)
    ax.set_xticks(range(*xrange) + [xrange[-1]])
    ax.set_ylim(*yrange)
    ax.set_yticks(range(*yrange) + [yrange[-1]])
    ax.set_aspect(1)


def plot_piece(ax, piece):
    """Helper - Plots a single game piece"""

    colour = piece.colour
    polygon = piece.polygon

    if polygon.type == 'Polygon':
        patch = PolygonPatch(
            polygon, facecolor=colour, edgecolor=shape_edge_colour, alpha=shape_alpha, zorder=2)
        ax.add_patch(patch)

    elif polygon.type == 'MultiPolygon':
        for poly in polygon.geoms:
            patch = PolygonPatch(
                poly, facecolor=colour, edgecolor=shape_edge_colour, alpha=shape_alpha, zorder=2)
            ax.add_patch(patch)

    if piece.id is not None:
        # Show piece ID
        centroid = piece.polygon.centroid
        s = str(piece.id)
        ax.text(centroid.x, centroid.y, s,
                horizontalalignment='center',
                verticalalignment='center',
                size=id_font_size)
