"""Print strings in columns.

A simple way to print short strings to a terminal in columns.

Unlike many similar utilities, it is NOT necessary for the strings to be
in a list before printing. column_print can print any sequence of strings
without knowing the length or number of strings in advance.


ColumnPrinter
-------------

A context manager class to print strings with padding to form columns.

Parameters
----------

columns : int, default=2
    The number of columns in layout.

width : int, default=80
    Total width of layout.
    If not supplied, column_print will attempt to read the width of the
    terminal (using shutil), and will fall back to 80 character with if
    the terminal with cannot be determined.


Note that if a string is longer than the width of a column, it will
occupy more than one column, and the next printed item will be shifted
to the next available column.

Example
-------

1. Initialise ColumnPrinter with no arguments::

    from column_print import ColumnPrinter
    with ColumnPrinter() as cp:
        cp("Hello")
        cp("World")
        cp("Goodbye")
        cp("Moon")

Prints::

    Hello                                    World
    Goodbye                                  Moon


2. Initialise ColumnPrinter with keyword arguments::

    from column_print import ColumnPrinter
    with ColumnPrinter(columns=3, width=60) as cp:
        cp("Hello")
        cp("World")
        cp("Goodbye")
        cp("Moon")

Prints::

    Hello               World               Goodbye
    Moon


3. Print unknown number of strings of unknown length::

    from string import ascii_letters
    from secrets import choice
    from random import randint
    from column_print import ColumnPrinter
    with ColumnPrinter(columns=3, width=70) as cprint:
        for i in range(randint(10, 20)):
            length = randint(1, 20)
            cprint(''.join(choice(ascii_letters) for _ in range(length)))

Prints::

    KPTyqazKuwoY           dGYCzBIAkju            aXQtXhw
    JvnTfKkzabb            mcjZvqvXLdG            IadYqxaZ
    cHm                    dReYhbhNkhEw           HaVaEkdjQNGHUIlywzjK
    PCHXF

"""


from shutil import get_terminal_size


class ColumnPrinter:
    """Context manager class for printing columns.

    Attributes
    ----------
    columns : int, default=2
        Number of columns in layout.
    width : int, default=80
        Total width of layout (in characters).
        If not supplied, ColumnPrinter attempts to calculate width of terminal.

    """
    def __init__(self, columns=2, width=None):
        self.columns = columns
        # default width to terminal with or 80 if width can't be determined.
        self.width = width
        if width is None:
            self.width = get_terminal_size().columns
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
        pad = 0
        if self._col_count + col_required < self.columns:
            pad = min(self.width, self._col_width * col_required)
        print(txt.ljust(pad), end='')
        # Increment column count.
        if self._col_count >= self.columns:
            self._col_count = col_required
        else:
            self._col_count +=  col_required

    def __exit__(self, exc_type, exc_value, exc_traceback):
        print('')
