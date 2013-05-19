#-------------------------------------------------------------------------------
# Name:        Tetris AI
# Purpose:     Artificial intelligence for Tetris
#
# Version:     Python 2.7
#
# Author:      Alex Louden
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

from copy import deepcopy
from pprint import pprint
from operator import attrgetter

from shapeops import num_useful_rotations
from plotting import plot_game

max_iteration_cost = 10
""" The maximum cost that we'll explore subsequent moves for """

class Weightings(object):
    area = 1
    centroid = 1
    rows_removed = -5
    height = 0
    gaps = 10

class Stats(object):
    pass

class Move(object):
    def __init__(self, game, piece, rotation, left):
        self.game = game

        # Store piece
        self.piece = deepcopy(piece)

        # Store where to drop piece
        self.left = left

        # Store cost - use .calculate_cost()
        self.cost = None

        self.stats = Stats()

        self.next_moves = []

    def __str__(self):
        if self.cost is not None:
            return "<Move: {0.piece} rot:{0.piece.rotation}"\
                " left:{0.left} cost:{0.cost:.2f}>".format(self)
        else:
            return "<Move: {0.piece} rot:{0.piece.rotation} left:{0.left}>".format(self)

    def __repr__(self):
        return str(self)

    def try_dropping(self):
        previous_height = self.game.height
        previous_num_gaps = self.game.count_gaps()

        # Try dropping piece
        self.game.drop(self.piece, self.left)

        rows_removed = self.game.check_full_rows()
        centroid, area = self.game.calculate_blocks_above_height(previous_height)
        num_gaps = self.game.count_gaps()
        height = self.game.height

##        name = 'scenario\\game_move_{0.piece.id}_{0.piece.rotation}_{0.left}'.format(self)
##        self.game.status = name
##        plot_game(self.game, name)

        # Remove piece
        self.game.pieces.pop()
        self.game.update_merged_pieces()
        self.game.height = self.game.calculate_height()

        # Store stats
        self.stats.rows_removed = rows_removed
        self.stats.centroid     = centroid
        self.stats.area         = area
        self.stats.gaps         = num_gaps - previous_num_gaps
        self.stats.height       = height - previous_height

##        print str(self)
##        print self.stats.__dict__


    def calculate_cost(self, weighting):
        cost = 0

        cost += weighting.area         * self.stats.area
        cost += weighting.centroid     * self.stats.centroid
        cost += weighting.rows_removed * self.stats.rows_removed
        cost += weighting.gaps         * self.stats.gaps
        cost += weighting.height       * self.stats.height

        self.cost = cost


def get_best_moves(game):
    """ Main smarts """

    moves = []

    # Pre-calculate which rotations are useful for each piece number (1-7)
    useful_rotations = {i: num_useful_rotations(i) for i in range(1, 8)}

    # Try default cost weightings
    weights = Weightings

    while game.input_queue:

        piece = game.input_queue.pop()
        best_by_cost = get_moves_and_weights(game, piece, weights, useful_rotations)

        print 'Possible moves for piece {}:'.format(piece.id)
##        pprint (best_by_cost)


        # TODO fix loops and remove repeated code

        piece = game.input_queue.pop()

        for move in best_by_cost:
            game.drop(move.piece, move.left)

            # Do next level
            move.next_moves = get_moves_and_weights(game, piece, weights, useful_rotations)

            game.pieces.pop()



        pprint (best_by_cost)


##        moves.append(Move(p, rotation, left))

    print moves

    return moves

def get_possible_moves(game, piece, rotations):
    possible_moves = []

    # For each rotation
    for rotation_id in rotations:
        p = piece
        p.rotate(rotation_id)

        # For each left position
        for left in range(game.width - piece.width + 1):
            m = Move(game, p, rotation_id, left)
            possible_moves.append(m)

    return possible_moves

def get_moves_and_weights(game, piece, weights, useful_rotations):

    rotations = useful_rotations[piece.num]
    possible_moves = get_possible_moves(game, piece, rotations)

    for pm in possible_moves:
        pm.try_dropping()
        pm.calculate_cost(weights)

    # Sort possible moves by cost (best first)
    best_by_cost = sorted(possible_moves, key=attrgetter('cost'))

    return best_by_cost