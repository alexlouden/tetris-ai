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

class TetrisGame():
    def __init__(self, pieces, width=11, bufsize=1):
        """Initialise the game board"""

        # List of TetrisPieces
        self.input_queue = pieces
        self.pieces = []

        # Game width
        self.width = width

        # Number of buffer positions
        self.bufsize = bufsize
        self.buffer = []

        # Active game height (aim is to minimise this)
        self.height = 0

        # Game status for plot title
        self.status = "Tetris"

    def solve(self):
        self.output = ""

class TetrisPiece():
    def __init__(self, num):
        """Initialise a piece"""
        self.num = num

        # Rotation - 0, 1=90, 2=180, 3=270
        self.rotation = 0

        # Position of piece, relative to bottom left corner of board
        self.left = 0
        self.bottom = 0

        # Piece shape and colour
        self.polygon = get_shape_polygon(self.num)
        self.colour = get_piece_colour(self.num)

def main():
    # Parse input file
    piece_numbers = read_input_file('exampleinput.txt')

    # Convert numbers to Tetris piece objects
    pieces = [TetrisPiece(n) for n in piece_numbers]

    # Initialise game with list of pieces
    game = TetrisGame(pieces)

    # Solve game
    game.solve()

    print game.height

    # Write output of game moves
    write_output_file('output.txt', game.output)

if __name__ == '__main__':
    main()
