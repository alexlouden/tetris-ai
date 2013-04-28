tetris-ai
=========

Written by Alex Louden - 20255851

<table>
  <tr>
    <th>Name</th><th>Student Number</th>
  </tr>
  <tr>
    <td>Alex Louden</td><td>20255851</td>
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

 * tetris.py - The main script
 * test_tetris.py - Testing and calculations
 * plotting.py - Plotting functionality
 * fileops.py - File operations
 * shapeops.py - Shape operations
