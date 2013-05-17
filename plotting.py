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
from shapely.affinity import translate
from descartes.patch import PolygonPatch

figure_size = (8, 10)
shape_edge_colour = '#000000'
shape_alpha = 0.8
id_font_size = 10

def plot_game(game, filename=None):
    """Plots the tetris game.

    Plot to file if a filename is given, otherwise plot to the screen.
    """

    # Create figure and axis
    pyplot.clf()
    fig = pyplot.figure(1, figsize=figure_size, dpi=90)
    ax = fig.add_subplot(111)

    # Plot the board and pieces
    plot_board(ax, game)
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

        pyplot.savefig(filename)

def plot_board(ax, game):
    """Helper - Plots the game board"""

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
    """Helper - Plots a single game piece"""

    colour = piece.colour
    polygon = piece.polygon

    # Move polygon to left/bottom pos
    # polygon = translate(polygon, xoff=piece.left, yoff=piece.bottom)

    patch = PolygonPatch(polygon, facecolor=colour, edgecolor=shape_edge_colour, alpha=shape_alpha, zorder=2)
    ax.add_patch(patch)

    if piece.id is not None:
        # Show piece ID
        centroid = piece.polygon.centroid
        s = str(piece.id)
        ax.text(centroid.x+piece.left, centroid.y+piece.bottom, s,
            horizontalalignment='center',
            verticalalignment='center',
            size=id_font_size)

if __name__ == "__main__":
    main()
