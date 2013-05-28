tetris-ai
=========

<table>
  <tr>
    <th>Name</th><th>Student Number</th>
  </tr>
  <tr>
    <td>Alex Louden</td><td>20255851</td>
  </tr>
  <tr>
    <td>Ruvan Muthu-Krishna</td><td>20507884</td>
  </tr>
</table>

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

 * ai.py - AI player
 * fileops.py - File operations
 * plotting.py - Plotting functionality
 * shapeops.py - Shape operations
 * test_scenario.py - Game scenario testing and calculations
 * test_tetris.py - Testing and calculations
 * tetris.py - The main script

### Ai.py

Mimics a Tetris player by using search algorithms to find the optimal set of moves. Manipulates a TetrisGame object.

### Fileops.py

Reads input file and populates a list of recognised pieces. Outputs an ordered optimal set of moves as determined by ai.py.

### Plotting.py

Plots Tetris game, either to the screen or to disk, including board and pieces placed.

### Shapops.py

Define valid TetrisPiece colour and starting geometry. Provide functions for moving, rotating, splitting and merging TetrisPieces.
Calculate the number of unique rotations of each TetrisPiece so that search trees can be minimised.

### Test_scenario.py

Game scenario tests to verify correct execution of program modules.

### Test_tetris.py

Unit tests to verify correct execution of program functions.

### Tetris.py

Holds TetrisGame and TetrisPiece classes which are used to build a Tetris game. TetrisGame stores Tetris game variables and functions needed to play a Tetris game.


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


Problem Definition
------------------
Tetris-AI aims to provide an AI solution to the classic game of Tetris. During play tetriminoes are dropped into a grid,
the user aims to move and tessellate them such that the overall game height is kept below a pre-defined line.
The CITS4211 implementation of the game allows for a semi-infinite rectangular game space of w units wide and no upper limit.
Thus the only end state of this game is when all tetriminoes stored in the queue have been placed and the only goal is to
minimise the height of the tetriminoes at the end state.

The CITS4211 implementation also allows for a 'hold' or buffer where a single tetrimino is allowed to be stored and used at
a later stage in the game.

There are seven unique tetriminoes and each has a certain number of unique rotations it can perform based on its geometry
and the fact that rotation can only be in discrete multiples of 90 degrees.

Each time a row becomes completely filled with tetriminoes, the row is removed and all pieces above it are moved down by
one unit.

Program Input
-------------
Is in the form of a text file containing the valid characters [1,7] to define the starting tetrimino queue.
Fileops.py reads the input text file while ignoring any invalid characters and all characters following an invalid character on the same line.

Program Solution
----------------
The current version of Tetris-AI makes the following assumptions:
- Tetriminoes cannot be horizontally translated after their initial left-point is set.
- The tetrimino queue does not have to contain randomised 'bags' of tetriminoes, it instead can be completely random.

Tetris-AI employs the 2D spatial analysis package 'Shapely' for game play rather than a grid based system, one advantage
of this being that tetriminoes are not restricted to being composed of squares in order to correctly function.




Program Output
--------------

