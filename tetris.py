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

from shapeops import get_shape_polygon, get_piece_colour
from shapeops import merge, move, rotate, combine_split
from shapeops import get_row_box, get_single_box, get_height_box

from plotting import plot_game
from ai import get_best_moves

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
        self.update_merged_pieces()

    def solve(self):
        """Attempt to solve the game.

        Will move pieces from input_queue to pieces one by one.
        """
        print 'Starting to solve'
        print 'Number of pieces in input_queue:', len(self.input_queue)

        index = 0

        # Run the main artificial intelligence function
        moves = get_best_moves(self)

        for move in moves:
            piece = move.piece
            piece.rotate(move.rotation)

            self.drop(piece, left=move.left)

            plot_game(self, 'game_step_{}'.format(index))
            index += 1

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
        return "\n".join(["{0.num} {0.rotation} {0.left}".format(p) for p in self.pieces])

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
            intersected = False

            # Top to bottom
            for bottom in xrange(int(y_max)-1, int(y_min)-1, -1):
                box = get_single_box(left, bottom)

                # If the square contains a piece
                area_of_intersection = box.intersection(self.merged_pieces).area

                # print area_of_intersection, left, bottom, intersected

                if area_of_intersection != 0:
                    intersected = True
                else:
                    # If this isn't the first intersection we've seen
                    # (therefore we're underneath a piece)
                    if intersected:
                        gap_count += 1 - area_of_intersection

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


class TetrisPiece(object):
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
        x_min, y_min, x_max, y_max = self.polygon.bounds
        return int(x_max - x_min)

    @property
    def height(self):
        """Calculate polygon height"""
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
        return "<Piece {0.id}>".format(self)

    def __repr__(self):
        return str(self)

def main():
    # Parse input file
    piece_numbers = read_input_file('exampleinput.txt')

    # Convert numbers to Tetris piece objects
    pieces = [TetrisPiece(n, i) for i, n in enumerate(piece_numbers)]

    # Initialise game with list of pieces
    game = TetrisGame(pieces)

    # Solve game
    game.solve()
##
    print 'Game height:', game.height

    print game.get_output()
##
##    # Write output of game moves
##    write_output_file('output.txt', game.get_output())

if __name__ == '__main__':
    main()
