#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Test ColumnPrinter class."""


from column_print import ColumnPrinter


print('****************')
print('Three column')
print('60 char width')
print('****************')


with ColumnPrinter(3,60) as cp:
    cp("Hello")
    cp("World")
    cp("Goodbye")
    cp("Moon")
    cp("Hello")
    cp("World")
    cp("Goodbye")
    cp("Moon")
