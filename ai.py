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

class Move(object):
    def __init__(self, piece, rotation, left):
        self.piece = piece
        self.rotation = rotation
        self.left = left

    def __str__(self):
        return "{0.piece 0.rotation 0.left}".format(self)

def get_best_moves(game):

    moves = []

    while game.input_queue:

        p = game.input_queue.pop()
        rotation = 0
        left = 3

        moves.append(Move(p, rotation, left))

    return moves

def astart():
    pass

def brute_force():
    pass