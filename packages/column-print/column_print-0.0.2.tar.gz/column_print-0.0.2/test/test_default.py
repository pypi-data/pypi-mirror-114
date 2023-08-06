#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Test ColumnPrinter class with default settings."""


from column_print import ColumnPrinter


print('****************')
print('Two column test:')
print('****************')

with ColumnPrinter() as cp:
    cp("Hello")
    cp("World")
    cp("Goodbye")
    cp("Moon")
    cp("Now is the time for all good men")
    cp("to come to the aid of the party.")
    cp("Goodbye")
    cp("Now is the time for all good men to come to the aid of the party.")
    cp("Moon")
    cp("Hello")
    cp("World")
    cp("Goodbye")
    cp("Moon")
