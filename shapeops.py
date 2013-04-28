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

from shapely.geometry import Polygon

# List of shape coordinates - (x,y)
piece_shapes = {
    1: [(0,0), (1,0), (1,4), (0,4), (0,0)],
    2: [(0,0), (2,0), (2,2), (0,2), (0,0)],
    3: [(0,0), (0,3), (1,3), (1,2), (2,2), (2,1), (1,1), (1,0), (0,0)],
    4: [(0,0), (0,3), (2,3), (2,2), (1,2), (1,0), (0,0)],
    5: [(0,2), (0,3), (2,3), (2,0), (1,0), (1,2), (0,2)],


}

def get_shape_polygon(number):
    return Polygon(piece_shapes.get(number, piece_shapes.get(2)))

piece_colours = {
    1: '#ff0000',
    2: '#de60cc',
    3: '#f79646',
    4: '#ffff00',
    5: '#00b050',
    6: '#66ffff',
    7: '#4f81bd'
}

def get_piece_colour(number):
    return piece_colours.get(number)