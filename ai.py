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
from collections import defaultdict
import sys

from shapeops import num_useful_rotations
from plotting import plot_game

useful_rotations = {}
""" Associate rotations with piece IDs - calculated once """

class Weightings(object):
    def __init__(self):
        """Hold weights associated with each aspect of the cost function."""
        self.area = 1       # Area of piece above previous game height
        self.centroid = 1   # Height of centroid above previous game height
        self.height = 5     # Change in game height
        self.rows_removed = -10
        self.gaps = 2
        self.centroidy = 0.5

        self.starting_score = self.rows_removed * -4 # Ensure no negative scores
        self.max_iteration_cost = 65 # TODO fix - use median/minimum etc?

        self.best_cost_at_depth = {}
        """ The best cost encountered at any tree depth """

class Stats(object):
    pass

class Move(object):
    """Hold a possible move to be made.

    Keyword arguments:
    game -- the game in which the piece will be placed
    piece -- the piece the move will place
    rotation -- rotation id of piece
    left -- where to drop the piece

    """
    def __init__(self, game, piece, rotation, left):
        self.game = game

        # Store piece
        self.piece = deepcopy(piece)

        # Store where to drop piece
        self.left = left

        # Store cost - use .calculate_cost()
        self.cost = None

        self.stats = Stats()

    def __str__(self):
        if self.cost is not None:
            return "<Move: {0.piece} rot:{0.piece.rotation}"\
                " left:{0.left} cost:{0.cost:.2f}>".format(self)
        else:
            return "<Move: {0.piece} rot:{0.piece.rotation} left:{0.left}>".format(self)

    def __repr__(self):
        return str(self)

    def try_dropping(self):
        """Drop piece into game, record change in game variables such as the
        number of gaps and the game height.

        Record how many rows were removed as a result of the drop and the
        position of the centroid of the dropped piece its area above the
        previous maximum game height."""

        previous_height = self.game.height
        previous_num_gaps = self.game.count_gaps()

        # Try dropping (copy of) piece
        self.game.drop(deepcopy(self.piece), self.left)

        rows_removed = self.game.check_full_rows()
        centroid, area = self.game.calculate_blocks_above_height(previous_height)
        num_gaps = self.game.count_gaps()
        height = self.game.height

##        name = 'scenario\\game_move_{0.piece.id}_{0.piece.rotation}_{0.left}'.format(self)
##        self.game.status = name
##        plot_game(self.game, name)

        # Store stats
        self.stats.rows_removed = rows_removed
        self.stats.centroid     = centroid
        self.stats.area         = area
        self.stats.gaps         = num_gaps - previous_num_gaps
        self.stats.height       = height - previous_height
        self.stats.centroidy    = self.piece.polygon.centroid.y

        # Remove piece (TODO: tidy up)
        self.game.pieces.pop()
        self.game.update_merged_pieces()
        self.game.height = self.game.calculate_height()

##        print str(self)
##        print self.stats.__dict__

    def calculate_cost(self, weights):
        """ Return cost of move given move stats and weightings """
        cost = 0

        cost += weights.area         * self.stats.area
        cost += weights.centroid     * self.stats.centroid
        cost += weights.rows_removed * self.stats.rows_removed
        cost += weights.gaps         * self.stats.gaps
        cost += weights.height       * self.stats.height
        cost += weights.centroidy    * self.stats.centroidy

        cost += weights.starting_score

        self.cost = cost



class Step(object):

    def __init__(self, game, depth=0, cost=0, move=None, weights=None):

        self.game = game
        self.children = []
        self.depth = depth
        self.cumulative_cost = cost
        self.move = move

        # No more moves to make
        if not self.game.input_queue:
            self.piece = None
            print "End node! ", cost
            return

        # Get next piece
        self.piece = self.game.input_queue.pop()

##        print 'Possible moves for piece {}:'.format(piece.id)

        # Determine possible moves
        possible_moves = self.get_possible_moves()

        # Get move weightings
        for pm in possible_moves:
            pm.try_dropping()
            pm.calculate_cost(weights)

        # Sort possible moves by cost (best first)
        best_by_cost = sorted(possible_moves, key=attrgetter('cost'))

        # Moves to make
        for move in best_by_cost:

            # Only make some moves
            if move.cost > weights.max_iteration_cost:
##                print 'Skipping due to max_iteration_cost', move.cost
                continue

            if not self.is_best_cost(depth, move.cost + self.cumulative_cost, weights):
                continue

            new_game = deepcopy(self.game)
            new_game.drop(move.piece, move.left)

            # Iterate down
            child = Step(new_game,
                self.depth + 1,
                self.cumulative_cost + move.cost,
                move, weights=weights)
            self.children.append(child)

    def __str__(self):
        if self.piece:
            return "<Step: id:{0.piece.id} depth:{0.depth} cost:{0.cumulative_cost:.2f}>".format(self)
        else:
            return "<Step: end depth:{0.depth} cost:{0.cumulative_cost:.2f}>".format(self)

    def __repr__(self):
        return str(self)

    def get_possible_moves(self):
        """ Return all possible moves given the game state and piece. """

        possible_moves = []

        rotations = useful_rotations[self.piece.num]

        # For each rotation
        for rotation_id in rotations:
            p = self.piece
            p.rotate(rotation_id)

            # For each left position
            for left in range(self.game.width - self.piece.width + 1):
                m = Move(self.game, p, rotation_id, left)
                possible_moves.append(m)

        return possible_moves

    def is_best_cost(self, depth, cost, weights):

        # Check best_score_at_depth
        best_cost = weights.best_cost_at_depth.get(depth)

        if best_cost is None:
            # New best cost for this depth

            weights.best_cost_at_depth[depth] = cost
            print 'First best_cost created', cost, depth
            return True

        elif cost > best_cost:
            # Skip - return False

##            print 'Skipping, best encountered previously', cost, depth
            return False

        else:
            # Set new best cost
##            print 'New best', cost, depth
            weights.best_cost_at_depth[depth] = cost
            return True


def get_best_moves(game, lookahead_distance=3, step_distance=2):
    """ Main smarts """

    # Pre-calculate which rotations are useful for each piece number (1-7)
    global useful_rotations # Global to have shared amongst all Steps
    useful_rotations = {i: num_useful_rotations(i) for i in range(1, 8)}

    weights = Weightings()

    # Copy the game's queue
    piece_queue = deepcopy(game.input_queue)

    # List to remember the moves we make
    moves = []
    moves_made = 0

    while moves_made < len(piece_queue):

        # Set input queue to just first lookahead_distance pieces (from end)
        start_index = - lookahead_distance - moves_made
        end_index = - moves_made if moves_made > 0 else None
        game.input_queue = deepcopy(piece_queue[start_index:end_index])

        print "Input queue:", game.input_queue

        # Can finish game now
        if moves_made + len(game.input_queue) == len(piece_queue):
            step_distance = len(game.input_queue)
            print 'Finish him!'

        # Step through pieces
        step = Step(game, weights=weights)


        # Make step_distance moves down tree in best direction
        for i in range(step_distance):

            if not step.children:
                print 'End reached'
                break

            # Go to next step
            step = step.children[0]

            moves.append(step.move)
            moves_made += 1

            print 'Move:', step.move



        # Use game state
        game = step.game








    while step.children:

        # Iterating down
        step = step.children[0]

        moves.append(step.move)

    print 'Moves:'
    pprint(moves)

    pprint(weights.best_cost_at_depth)

    return moves









