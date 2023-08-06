"""Utilities to print strings in columns.

This module contains utilities to simplify printing to a Terminal in columns. 

ColumnPrinter
-------------

A context manager class to print strings with padding to form columns.

Parameters
----------

columns : int, default=2
    The number of columns in layout.

width : int, default=80
    Total width of layout.


Note that if a string is longer than the width of a column, it will
occupy more than one column, and the next printed item will be shifted
to the next available column.

Example
-------

1. Initialise ColumnPrinter with no arguments::

    from modules.column_print import ColumnPrinter
    
    with ColumnPrinter() as cp:
        cp("Hello")
        cp("World")
        cp("Goodbye")
        cp("Moon")

Prints::

    Hello                                    World
    Goodbye                                  Moon


2. Initialise ColumnPrinter with arguments::


    from modules.column_print import ColumnPrinter
    
    with ColumnPrinter(columns=3) as cp:
        cp("Hello")
        cp("World")
        cp("Goodbye")
        cp("Moon")

Prints::

    Hello                       World                       Goodbye
    Moon

"""

class ColumnPrinter:
    """Context manager class for printing columns.

    Attributes
    ----------
    columns : int
        Number of columns in layout.
    width : int
        Total width of layout (in characters).

    """
    def __init__(self, columns=2, width=80):
        self.columns = columns
        self.width = width
        self._col_count = 0
        self._col_width = self.width // self.columns

    def __enter__(self):
        return self

    def __call__(self, txt):
        """Print in columns."""
        col_required = 1 + (len(txt) // self._col_width)
        col_remain = self.columns - self._col_count
        # If can't fit on line, start new line.
        if col_required > col_remain:
            print('')
            self._col_count = 0
        # If not filling line, calculate padding.
        if self._col_count + col_required < self.columns:
            pad = min(self.width, self._col_width * col_required)
        else:
            pad = 0
        print('{:<{width}s}'.format(txt, width=pad), end='')
        # Increment column count.
        if self._col_count >= self.columns:
            self._col_count = col_required
        else:
            self._col_count +=  col_required

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('')
