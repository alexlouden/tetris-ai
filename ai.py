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
    """Hold weights associated with each aspect of the cost function."""

    bignum = sys.maxint

    area = 1       # Area of piece above previous game height
    centroid = 1   # Height of centroid above previous game height
    height = 2     # Change in game height
    rows_removed = -10
    gaps = 5
    centroidy = 0.5

    lookahead_distance = 3
    step_distance = 2

    starting_score = rows_removed * -4 # Ensure no negative scores

    best_endstep_cost = bignum
    """ The best cost encountered at the leaves of a tree """

    best_cost_at_depth  = {}
    worst_cost_at_depth = {}

    maximum_percentage = 0.1
    """ Percentage difference for passable cost in range from best to worst previously found costs """

    minimum_diff = 4
    """ Minimum difference between previously found minimum cost and passable cost """

    def skip_move(self, depth, cost):

        best = self.best_cost_at_depth[depth]
        worst = self.worst_cost_at_depth[depth]

        max_cost = max((worst - best) * self.maximum_percentage + best,
                       best + self.minimum_diff)

        return not best <= cost <= max_cost


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
        self.best_child = None

        # No more moves to make - this is end node
        if not self.game.input_queue:
            self.piece = None
            self.best_cost = self.cumulative_cost

            # Set new best endstep cost if needed
            weights.best_endstep_cost = min(weights.best_endstep_cost, cost)

##            if weights.best_endstep_cost == cost:
##               print "Best new end node! ", cost

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

        # Prune moves, based on their cost
        best_by_cost = self.prune_moves(best_by_cost, weights)

        # Moves to make
        for move in best_by_cost:

            if move.cost + self.cumulative_cost >= weights.best_endstep_cost:
##                print 'Skipping due to best_endstep_cost', move.cost + self.cumulative_cost
##                print 'Skip depth: ', self.depth
                continue

            new_game = deepcopy(self.game)
            new_game.drop(move.piece, move.left)

            # Iterate down
            child = Step(new_game,
                self.depth + 1,
                self.cumulative_cost + move.cost,
                move, weights=weights)

            self.children.append(child)

        # Reference to the best child
        if self.children:
            self.best_child = min(self.children, key=attrgetter('best_cost'))
            self.best_cost = self.best_child.best_cost

        else:
            # Best cost encountered (but not explored)
            self.best_cost = self.cumulative_cost

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

    def prune_moves(self, moves, weights):

        best_cost = moves[0].cost
        worst_cost = moves[-1].cost

        current_best = weights.best_cost_at_depth.get(self.depth)


        if current_best is None:
            # First time at depth
            weights.best_cost_at_depth[self.depth] = best_cost
        else:
            # Update
            weights.best_cost_at_depth[self.depth] = min(current_best, best_cost)
##            print 'New best cost for depth', self.depth, current_best, '->' ,best_cost

        try:
            weights.worst_cost_at_depth[self.depth] = max(weights.worst_cost_at_depth[self.depth], worst_cost)
        except KeyError:
            weights.worst_cost_at_depth[self.depth] = worst_cost

##        print 'prune:', self.depth, best_cost, worst_cost, current_best, weights.worst_cost_at_depth.get(self.depth)

        return [move for move in moves if not weights.skip_move(self.depth, move.cost)]


def get_best_moves(game):
    """ Main smarts """

    # Pre-calculate which rotations are useful for each piece number (1-7)
    global useful_rotations # Global to have shared amongst all Steps
    useful_rotations = {i: num_useful_rotations(i) for i in range(1, 8)}

    weights = Weightings()

##    print 'Using a lookahead of {} with a step of {}'.format(
##        weights.lookahead_distance, weights.step_distance)

    # Copy the game's queue
    piece_queue = deepcopy(game.input_queue)

    # List to remember the moves we make
    moves = []
    moves_made = 0

    while moves_made < len(piece_queue):

        # Set input queue to just first lookahead_distance pieces (from end)
        start_index = - weights.lookahead_distance - moves_made
        end_index = - moves_made if moves_made > 0 else None
        game.input_queue = deepcopy(piece_queue[start_index:end_index])

##        print "Input queue:", game.input_queue

##        print 'Numbers:', moves_made, len(game.input_queue), len(piece_queue)

        # Can finish game now
        if moves_made + len(game.input_queue) == len(piece_queue):
            weights.step_distance = len(game.input_queue)
##            print 'Finish him!', weights.step_distance

        weights.best_endstep_cost = weights.bignum
        weights.best_cost_at_depth = {}
        weights.worst_cost_at_depth = {}

        # Step through pieces
        step = Step(game, depth=moves_made, weights=weights)

        # Make step_distance moves down tree in best direction
        for i in range(weights.step_distance):

            if not step.best_child:
##                print 'End reached'
##                print step
                break

            # Go to next step
            step = step.best_child

            moves.append(step.move)
            moves_made += 1

##            print 'Move:', step.move

        # Use game state
        game = step.game


##    print 'Moves:'
##    pprint(moves)

    return moves









