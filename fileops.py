#-------------------------------------------------------------------------------
# Name:        Tetris File Operations
# Purpose:     Functions to read and write to disk
#
# Version:     Python 2.7
#
# Author:      Alex Louden
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden 2013
# Licence:     MIT
#-------------------------------------------------------------------------------

from shapeops import valid_shape_id

def read_input_file(filename):

    # An empty list to contain our input numbers
    numbers = []

    # Open input file in read only mode
    with open(filename, 'r') as f:
        # Iterate through each line in the file
        for line in f:
            # Use list comprehension to filter only character digits
            # Then convert each character to an integer
            digitsonly = [int(char) for char in line if char.isdigit()]

            # Strip out zeros
            nozeros = [i for i in digitsonly if valid_shape_id(i)]

            # And add these numbers to the list
            numbers.extend(nozeros)

    return numbers

def write_output_file(filename, output):

    # Open output file in write mode
    with open(filename, 'w') as f:
        f.write(output)


