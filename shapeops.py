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

from shapely.geometry import Polygon, Point
from shapely.affinity import rotate
from shapely.ops import cascaded_union

# List of shape coordinates - (x,y)
piece_shapes = {
    1: [(0,0), (1,0), (1,4), (0,4), (0,0)],
    2: [(0,0), (2,0), (2,2), (0,2), (0,0)],
    3: [(0,0), (0,3), (1,3), (1,2), (2,2), (2,1), (1,1), (1,0), (0,0)],
    4: [(0,0), (0,3), (2,3), (2,2), (1,2), (1,0), (0,0)],
    5: [(0,2), (0,3), (2,3), (2,0), (1,0), (1,2), (0,2)],
    6: [(0,1), (0,3), (1,3), (1,2), (2,2), (2,0), (1,0), (1,1), (0,1)],
    7: [(0,0), (0,2), (1,2), (1,3), (2,3), (2,1), (1,1), (1,0), (0,0)],
}

def get_shape_polygon(num):
    return Polygon(piece_shapes[num])

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

def get_piece_colour(num):
    return piece_colours[num]

# Whether shape ID is valid - has both colour and shape
# Used in parsing input file
def valid_shape_id(num):
    return num in piece_colours and num in piece_shapes

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

    for rotation_id in range(1,5):
        # Angle of rotation in degrees
        angle = rotation_id * 90

        rotated_piece = rotate(shape, angle, origin='centroid')

        # Make sure rotated piece isn't same as an existing unique shape
        if not any(rotated_piece.equals(shape) for shape in unique_rotation_shapes):
            unique_rotation_states.append(rotation_id)
            unique_rotation_shapes.append(rotated_piece)

    return unique_rotation_states



def merge_pieces(pieces):
    if not pieces:
        return Polygon()

    return cascaded_union([p.polygon for p in pieces])
