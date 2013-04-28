#-------------------------------------------------------------------------------
# Name:        Tetris AI
# Purpose:
#
# Author:      Alex Louden
#
# Created:     28/04/2013
# Copyright:   (c) Alex Louden 2013
# Licence:
#-------------------------------------------------------------------------------

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
            nozeros = [i for i in digitsonly if i > 0]

            # And add these numbers to the list
            numbers.extend(nozeros)

    return numbers

def main():
    print read_input_file('exampleinput.txt')

if __name__ == '__main__':
    main()
