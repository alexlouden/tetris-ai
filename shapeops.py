#-------------------------------------------------------------------------
# Name:        Shape Operations
# Purpose:     Functions to perform shape operations on pieces and the game
#
# Version:     Python 2.7
#
# Author:      Alex Louden
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden 2013
# Licence:     MIT
#-------------------------------------------------------------------------

from shapely.geometry import Polygon, box
from shapely.affinity import translate, rotate as polygon_rotate
from shapely.ops import cascaded_union

"""
Houses all code for the shape operations used by tetris.py

"""


class Pieces(object):

    # List of shape coordinates - (x,y)
    piece_shapes = {
        1: [(0, 0), (1, 0), (1, 4), (0, 4), (0, 0)],
        2: [(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)],
        3: [(0, 0), (0, 3), (1, 3), (1, 2), (2, 2), (2, 1), (1, 1), (1, 0), (0, 0)],
        4: [(0, 0), (0, 3), (2, 3), (2, 2), (1, 2), (1, 0), (0, 0)],
        5: [(0, 2), (0, 3), (2, 3), (2, 0), (1, 0), (1, 2), (0, 2)],
        6: [(0, 1), (0, 3), (1, 3), (1, 2), (2, 2), (2, 0), (1, 0), (1, 1), (0, 1)],
        7: [(0, 0), (0, 2), (1, 2), (1, 3), (2, 3), (2, 1), (1, 1), (1, 0), (0, 0)],
    }

    # Hex colours for plotting
    piece_colours = {
        1: '#ff0000',
        2: '#de60cc',
        3: '#f79646',
        4: '#ffff00',
        5: '#00b050',
        6: '#66ffff',
        7: '#4f81bd'
    }


def get_shape_polygon(num):
    return Polygon(Pieces.piece_shapes[num])


def get_piece_colour(num):
    return Pieces.piece_colours[num]


def valid_shape_id(num):
    """ Check whether shape ID is valid - has both colour and shape
        Used in parsing input file
    """
    return num in Pieces.piece_colours and num in Pieces.piece_shapes


def num_useful_rotations(num):
    """ Determine which rotation states are unique

    i.e.
        piece 1 (line)   = [0, 90]
        piece 2 (square) = [0]
        piece 3          = [0, 90, 180, 270]
    """

    shape = get_shape_polygon(num)

    unique_rotation_states = [0]
    unique_rotation_shapes = [shape]

    for rotation_id in range(1, 5):
        # Angle of rotation in degrees
        angle = rotation_id * 90

        rotated_piece = polygon_rotate(shape, angle, origin='centroid')

        # Make sure rotated piece isn't same as an existing unique shape
        if not any(rotated_piece.equals(shape) for shape in unique_rotation_shapes):
            unique_rotation_states.append(rotation_id)
            unique_rotation_shapes.append(rotated_piece)

    return unique_rotation_states


def merge(pieces):
    if not pieces:
        return Polygon()

    return cascaded_union([p.polygon for p in pieces])


def move(polygon, x, y):
    return translate(polygon, x, y)


def rotate(polygon, angle):
    centre_of_rotation = (0, 0)
    return polygon_rotate(polygon, angle, origin=centre_of_rotation)


def get_row_box(width, bottom):
    return box(0, bottom, width, bottom + 1)


def get_single_box(left, bottom):
    return box(left, bottom, left + 1, bottom + 1)


def get_box(*args):
    return box(*args)


def get_height_box(width, height):
    return box(0, 0, width, height)


def combine_split(shape):
    """Combine a MultiPolygon into a single shape"""
    shape1, shape2 = shape.geoms

    # Drop the higher shape down by 1 row
    if shape1.centroid.y > shape2.centroid.y:
        shape1 = translate(shape1, yoff=-1)
    else:
        shape2 = translate(shape2, yoff=-1)

    return shape1.union(shape2)
