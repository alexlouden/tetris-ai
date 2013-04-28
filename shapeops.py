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

def get_shape_polygon(number):
    return Polygon([(0,0), (2,0), (2,2), (0,2), (0,0)])

def get_piece_colour(number):

    return '#FF000'