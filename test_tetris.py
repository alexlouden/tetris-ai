#-------------------------------------------------------------------------------
# Name:        Tetris Tests
# Purpose:
#
# Author:      Alex
#
# Created:     28/04/2013
# Copyright:   (c) Alex 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import nose
from nose.tools import timed, raises, assert_equals

def test_read_input_file():

    from fileops import read_input_file

    actual = read_input_file('exampleinput.txt')
    expected = [1, 2, 3, 4, 5, 2, 7, 1, 6, 1, 8, 9, 4, 3, 2, 1, 5]

    assert_equals(actual, expected)


def test_write_output_file():
    pass

if __name__ == '__main__':
    nose.main(argv=[
        '--failed',
        '--verbosity=2',
##        '--nocapture'
        ])
