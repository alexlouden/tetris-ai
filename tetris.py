#-------------------------------------------------------------------------------
# Name:        Tetris AI
# Purpose:     Holds TetrisGame and TetrisPiece classes
#              which are used to build a Tetris game
#
# Version:     Python 2.7
#
# Author:      Alex Louden
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden 2013
# Licence:     MIT
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from copy import deepcopy
import argparse
from pprint import pprint
import os
from time import clock, time
# Choose higher resolution time counter
time = clock if os.name == 'nt' else time

from fileops import read_input_file, write_output_file

from shapeops import get_shape_polygon, get_piece_colour
from shapeops import merge, move, rotate, combine_split
from shapeops import get_row_box, get_single_box, get_height_box, get_box

from plotting import plot_game
from ai import get_best_moves, Weightings


class TetrisGame(object):
    """Store Tetris game variables and functions needed to play a Tetris game.
    Once game is setup, invoke ai.py to play the game.

    Keyword arguments:
    pieces -- a list of TetrisPieces (Tetriminoes)
    width -- the game width
    max_buffer_size -- maximum number of TetrisPieces able to be held in a temporary buffer

    """
    def __init__(self, pieces=None, width=11, max_buffer_size=1):
        """Initialise the game board"""

        # Check piece ids are unique
        self.validate_pieces(pieces)

        # List of TetrisPieces
        self.input_queue = pieces if pieces is not None else []
        self.input_queue.reverse()
        self.pieces = []

        # Game width
        self.width = width

        # Initial number of gaps
        self.num_gaps = 0

        # Active game height (aim is to minimise this)
        self.height = 0

        # Game status for plot title
        self.status = "Tetris"

        # Merge all pieces together into one polygon
        self.update_merged_pieces()

    def solve(self, num_threads=None):
        """Attempt to solve the game.

        Will move pieces from input_queue to pieces one by one.
        """
##        print 'Starting to solve'
##        print 'Number of pieces in input_queue:', len(self.input_queue)

        index = 0

        # Make a copy of the empty game state
        gamecopy = deepcopy(self)

        # Dictionary of pieces by ID
        pieces = {p.id:p for p in self.input_queue}

        # Run the main artificial intelligence function
        moves = get_best_moves(gamecopy, num_threads)

        # Store moves
        self.moves = moves

        for move in moves:
            piece_id = move.piece.id
            piece_rotation = move.piece.rotation
            piece_left = move.left

            # Get piece by it's ID
            piece = pieces.get(piece_id)

            # Rotate then drop it
            piece.rotate(piece_rotation)
            self.drop(piece, left=piece_left)

            # Plot before removing rows
            plot_game(self, '{}_step_{}'.format(self.status, index))

            # Plot after removing rows (if needed)
            rows_removed = self.check_full_rows()
            if rows_removed > 0:
                plot_game(self, '{}_step_{}b'.format(self.status, index))

            index += 1

        self.update_merged_pieces()
        self.height = self.calculate_height()

    def calculate_height(self):
        """Returns the max number of blocks from the bottom"""
        if self.merged_pieces.is_empty:
            return 0

        x_min, y_min, x_max, y_max = self.merged_pieces.bounds
        # Assume height is integer
        return int(y_max)

    def drop(self, piece, left):
        """ Drops piece into position x pixels from left.
        Ensure piece has been removed from input_queue first
        """

        # Validate whether piece will fit into game
        if piece.width + left > self.width:
            raise ValueError("Piece {0.id} is out of bounds".format(piece))

        piece.left = left
        piece.bottom = self.height

        # Drop down from top, one step at a time
        while piece.bottom > 0:
            piece.bottom -= 1

            # If piece intersects merged pieces, go back up one square
            if piece.intersects(self.merged_pieces):
                piece.bottom += 1
                break

        self.pieces.append(piece)

        self.update_merged_pieces()
        self.height = self.calculate_height()

    def get_output(self):
        return "\n".join(["{0.num} {0.rotation} {0.left:.0f}".format(m.piece) for m in self.moves])

    def update_merged_pieces(self):
        self.merged_pieces = merge(self.pieces)

    def check_full_rows(self):
        """Checks if any rows are full of pieces"""

        full_rows = []

        # Go through each row, add to list of full rows
        for height in range(0, self.height):
            if self.is_row_full(height):
                full_rows.append(height)

        # Go through each full row (top down)
        for row_id in full_rows[::-1]:
            self.remove_full_row(row_id)

        self.update_merged_pieces()
        self.height = self.calculate_height()

        # Return number of rows removed
        return len(full_rows)

    def is_row_full(self, height):
        """ Returns whether a row is completely full of pieces """
        row = get_row_box(self.width, height)
        return row.intersection(self.merged_pieces).area == row.area

    def remove_full_row(self, row_id):
        # Find out which shapes intersect this row and split them
        row = get_row_box(self.width, row_id)

        pieces_to_remove = []

        for index, piece in enumerate(self.pieces):
            # Split piece if it intersects row
            if piece.intersects(row):
                split_status = piece.split(row)

                if split_status == 'remove':
                    pieces_to_remove.append(piece)

            # Shift pieces above row down by one
            elif piece.polygon.centroid.y > row_id:
                piece.bottom -= 1

        # Remove all empty pieces
        for piece in pieces_to_remove:
            self.pieces.remove(piece)

    def count_gaps(self):
        # Count the gaps which cannot be filled by dropping a piece

        self.update_merged_pieces()

        # If no blocks yet
        if self.merged_pieces.is_empty:
            return 0

        x_min, y_min, x_max, y_max = self.merged_pieces.bounds


        gap_count = 0

        # Left to right
        for left in xrange(int(x_min), int(x_max)):

            # Top to bottom
            for bottom in xrange(int(y_max)-1, int(y_min)-1, -1):
                box = get_single_box(left, bottom)

                # If the square contains a piece
                area_of_intersection = box.intersection(self.merged_pieces).area

                if area_of_intersection != 0:

                    # Draw box from height down to zero, get single intersection area
                    box = get_box(left, 0, left + 1, bottom + 1)
                    gap_count += box.area - box.intersection(self.merged_pieces).area

                    break

        return gap_count


    def calculate_blocks_above_height(self, height):
        """ Returns a tuple of centroid, and area of blocks above height """

        # If no blocks yet
        if self.merged_pieces.is_empty:
            return 0, 0

        # If height is zero, all of merged_pieces are above line
        if height == 0:
            shape_above_height = self.merged_pieces

        else:
            # Get a polygon from 0 to height
            height_box = get_height_box(self.width, height)

            # Subtract merged pieces from height
            shape_above_height = self.merged_pieces.difference(height_box)

        if shape_above_height.is_empty:
            return 0, 0

        centroid = shape_above_height.centroid.y - height
        area = shape_above_height.area

        return centroid, area

    def validate_pieces(self, pieces):
        if pieces:
            s = {p.id for p in pieces}
            if len(s) != len(pieces):
                raise ValueError("Piece IDs are not unique")


class TetrisPiece(object):
    """Hold rotation, position and geometrical structure of a TetrisPiece. Provide functions to rotate, move, split and verify intersection of TetrisPiece.

    Keyword arguments:
    num -- defines the type of tetrimino TetrisPiece represents
    id -- position of TetrisPiece in queue as read from input file
    rotation -- rotational position

    """
    def __init__(self, num, id=None, rotation=0):
        """Initialise a piece"""
        self.num = num
        self.id = id

        # Position of piece, relative to bottom left corner of board
        self._left = 0
        self._bottom = 0

        # Piece shape and colour
        self.polygon = get_shape_polygon(self.num)
        self.colour = get_piece_colour(self.num)

        # Rotation - 0=0, 1=90, 2=180, 3=270
        self._rotation = 0
        self.rotation = rotation

    # Piece translation
    def move_to(self, left=None, bottom=None):
        """Move piece to a position.

        Keyword arguments:
        left -- the horizontal distance between the left game border and the left most position on the piece
        bottom -- the vertical distance between the bottom game border and the bottom most position of the piece

        """

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

    # Piece rotation
    def rotate(self, angle_id):
        """Rotate piece into rotation position 0,1,2,3"""

        if self.polygon.is_empty:
            raise ValueError("Polygon is empty")

        # Check angle_id is valid
        if angle_id not in range(0, 4):
            raise ValueError("Invalid angle id, must be one of 0, 1, 2 or 3")

        # Difference in angle
        angle_diff = angle_id*90 - self._rotation*90

        # Rotate polygon
        self.polygon = rotate(self.polygon, angle_diff)

        # Set rotation attribute
        self._rotation = angle_id

        previous_left = self.left
        previous_bottom = self.bottom

        # Update left/bottom
        self._left = self.polygon.bounds[0]
        self._bottom = self.polygon.bounds[1]

        # Move bottom left corner to where shape was before rotation
        self.move_to(previous_left, previous_bottom)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self.rotate(value)

    @property
    def width(self):
        """Calculate polygon width"""
        if self.polygon.is_empty:
            raise ValueError("Piece is empty. Why are you here?")

        x_min, y_min, x_max, y_max = self.polygon.bounds
        return int(x_max - x_min)

    @property
    def height(self):
        """Calculate polygon height"""
        if self.polygon.is_empty:
            raise ValueError("Piece is empty. Why are you here?")

        x_min, y_min, x_max, y_max = self.polygon.bounds
        return int(y_max - y_min)

    def intersects(self, other):
        """ Returns whether this piece intersects the other """
        return self.polygon.intersection(other).area != 0

    def split(self, row):
        """ Split shape by row polygon

        When shapes intersect the row, they are merged down.

        E.g.
              [ ]
        [x][x][x]  -->        [ ]
        [ ]             [ ]

        """
        shape = self.polygon.difference(row)

        if shape.type == 'MultiPolygon':
            # Combine multiple geoms into one
            shape = combine_split(shape)

        elif shape.type == 'Polygon':
            # If remaining polygon is above row
            if shape.centroid.y >= row.centroid.y:
                shape = move(shape, 0, -1)

        self.polygon = shape

        if self.polygon.is_empty:
            # Polygon is gone!
            return 'remove'

        # Update left/bottom attributes
        self._left = self.polygon.bounds[0]
        self._bottom = self.polygon.bounds[1]

    def __str__(self):
        return "<Piece {0.id} shape:{0.num}>".format(self)

    def __repr__(self):
        return str(self)

def solve_from_input_file(input_filename, output_filename=None,
        print_stats=False, num_threads=None):

    start_time = time()

    # Parse input file
    piece_numbers = read_input_file(input_filename)

    # Convert numbers to Tetris piece objects
    pieces = [TetrisPiece(n, i) for i, n in enumerate(piece_numbers)]

    # Initialise game with list of pieces
    game = TetrisGame(pieces)

    print '{} pieces loaded'.format(len(piece_numbers))
    print 'This will take approximately {} seconds. Sorry!'.format(len(piece_numbers)*5)

    # Solve game
    game.solve(num_threads)

    print 'Solving complete!'
    print 'Time taken: {:.2f}s'.format(time() - start_time)
    print 'Final game height:', game.height

    if print_stats:
        print '-'*40
        print 'Cost function weightings:'
        print '-'*40
        print Weightings()

        print '-'*40
        print 'Detailed statistics:'
        print '-'*40
        print 'Moves:'
        for move in game.moves:
            print move
            pprint(move.stats)

    if output_filename:
        # Write output of game moves
        write_output_file(output_filename, game.get_output())
    else:
        print '-'*40
        print 'Game output:'
        print '-'*40
        print game.get_output()


def parse_commandline_args():
    parser = argparse.ArgumentParser(description='Tetris-AI')

    parser.add_argument('input', type=str,
        help='the input filename containing Tetris piece IDs')

    parser.add_argument('output', type=str, nargs='?', default=None,
        help="""the output filename to write moves to.
        if this argument is missing, the program prints the moves to stdout.""")

    parser.add_argument('--stats', dest='stats', action="store_true",
        help='Show detailed statistics on game end state, moves and costs.')

    parser.add_argument('--threads', dest='threads', type=int, default=None,
        help="""Number of threads to spawn. If argument missing,
        program will automatically detect the number of CPU cores.""")

    args = parser.parse_args()

    solve_from_input_file(args.input, args.output, args.stats, args.threads)

if __name__ == '__main__':
    parse_commandline_args()

