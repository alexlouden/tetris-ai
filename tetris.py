#-------------------------------------------------------------------------------
# Name:        Tetris AI
# Purpose:     Solve tetris using AI
#
# Version:     Python 2.7
#
# Author:      Alex Louden
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

from fileops import read_input_file, write_output_file
from shapeops import get_shape_polygon, get_piece_colour, merge_pieces, move

from plotting import plot_game

class TetrisGame(object):
    def __init__(self, pieces=None, width=11, max_buffer_size=1):
        """Initialise the game board"""

        # List of TetrisPieces
        self.input_queue = pieces if pieces is not None else []
        self.input_queue.reverse()
        self.pieces = []

        # Game width
        self.width = width

        # Number of buffer positions
        self.max_buffer_size = max_buffer_size
        self.buffer = []

        # Active game height (aim is to minimise this)
        self.height = 0

        # Game status for plot title
        self.status = "Tetris"

        # Merge all pieces together into one polygon
        self.merged_pieces = merge_pieces(self.pieces)

    def solve(self):
        """Attempt to solve the game.

        Will move pieces from input_queue to pieces one by one.
        """
        print 'Starting to solve'
        print 'Number of pieces in input_queue:', len(self.input_queue)

        while self.input_queue:

            piece = self.input_queue.pop()
            self.step(piece)

##            plot_game(self, 'game_step_{}'.format(index))

    def step(self, piece):
        """Perform one game step"""
        print 'step', piece.id, piece.num
        # self.height = ?
        # self.buffer ?
        # piece.left = ?
        # piece.bottom = ?
        # self.pieces.append(piece)
##        raise NotImplementedError()

    def calculate_height(self):
        """Returns the max number of blocks from the bottom"""
        raise NotImplementedError()

    def is_valid(self):
        """Whether piece positions are valid"""
        raise NotImplementedError()

    def drop(piece, left):
        """ Drops piece into position x pixels from left.
        Ensure piece has been removed from input_queue first
        """
        # start at piece.top = self.height
        # drop down until one before intersection

        # Then put piece into game.pieces:
        # self.pieces.append(piece)
        raise NotImplementedError()

    def get_output(self):
        return "\n".join(["{0.num} {0.rotation} {0.left}".format(p) for p in self.pieces])

    def is_bottom_row_full(self):
        """Checks if bottom row is full of pieces"""

        raise NotImplementedError()


class TetrisPiece(object):
    def __init__(self, num, id=None):
        """Initialise a piece"""
        self.num = num
        self.id = id

        # Rotation - 0=0, 1=90, 2=180, 3=270
        self.rotation = 0

        # Position of piece, relative to bottom left corner of board
        self._left = 0
        self._bottom = 0

        # Piece shape and colour
        self.polygon = get_shape_polygon(self.num)
        self.colour = get_piece_colour(self.num)

    def rotate(self, num=0):
        """Rotate piece into rotation position 0,1,2,3"""
        # self.rotation = ??
        # self.polygon = ??
##        self.polygon = rotate()
        raise NotImplementedError()

    def move_to(self, left=None, bottom=None):

        # If attributes are None
        left = self.left if left is None else left
        bottom = self.bottom if bottom is None else bottom

        # Difference in position
        x_diff = left - self.left
        y_diff = bottom - self.bottom

        # Move polygon
        self.polygon = move(self.polygon, x_diff, y_diff)

        # Set position attributes
        self._left = left
        self._bottom = bottom

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self.move_to(left=value)

    @property
    def bottom(self):
        return self._bottom

    @bottom.setter
    def bottom(self, value):
        self.move_to(bottom=value)

    @property
    def width(self):
        """Calculate polygon width"""
        x_min, y_min, x_max, y_max = self.polygon.bounds
        return int(x_max - x_min)

    @property
    def height(self):
        """Calculate polygon height"""
        x_min, y_min, x_max, y_max = self.polygon.bounds
        return int(y_max - y_min)

def main():
    # Parse input file
##    piece_numbers = read_input_file('exampleinput.txt')

    # Convert numbers to Tetris piece objects
##    pieces = [TetrisPiece(n, i) for i, n in enumerate(piece_numbers)]

    pieces = [TetrisPiece(3, 'T'), TetrisPiece(4, 'Steve')]

    # Initialise game with list of pieces
    game = TetrisGame(pieces)

    # Solve game
    game.solve()
##
##    print game.height
##
##    # Write output of game moves
##    write_output_file('output.txt', game.get_output())

if __name__ == '__main__':
    main()
