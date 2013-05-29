tetris-ai
=========

Written by Alex Louden (@alexlouden) and Ruvan Muthu-Krishna. 

Description
-----------

We present an AI approach to solving tetris that can handle polygonal piece shapes.


Dependencies
------------

Python version 2.7 is used.

Several third party Python modules have been used for convenience, but the main program AI is written in plain Python.

 * [Shapely](http://toblerity.github.io/shapely/manual.html) - spatial analysis
 * [descartes](https://pypi.python.org/pypi/descartes) - plotting adapter for Shapely
 * [matplotlib](http://matplotlib.org/) - plotting
 * [numpy](http://numpy.scipy.org/) - numerical Python, required by matplotlib
 * [nose](https://nose.readthedocs.org/en/latest/) - unit testing

These packages can be installed using `pip` or `easy_install` on Linux/OSX, or via binaries on Windows.

Structure
---------

The program is structured into a number of Python files:

 * tetris.py - The main script
 * ai.py - AI algorithm
 * fileops.py - File operations
 * plotting.py - Plotting functionality
 * shapeops.py - Shape operations and definitions

Testing:
 * test_scenario.py - Game scenario testing and calculations
 * test_tetris.py - Testing and calculations
 * report.py - plots for the report
 * benchmark.py - performance benchmarking 

Usage
-----

    $ python tetris.py -h
    usage: tetris.py [-h] [--stats] [--threads THREADS] input [output]

    Tetris-AI

    positional arguments:
      input              the input filename containing Tetris piece IDs
      output             the output filename to write moves to. if this argument
                         is missing, the program prints the moves to stdout.

    optional arguments:
      -h, --help         show this help message and exit
      --stats            Show detailed statistics on game end state, moves and
                         costs.
      --threads THREADS  Number of threads to spawn. If argument missing, program
                         will automatically detect the number of CPU cores.

