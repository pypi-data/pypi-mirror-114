# -*- coding: utf-8 -*-
"""Module init-file.

A module's __name__ is set equal to '__main__' when read from standard input,
a script, or from an interactive prompt.
"""
from key_set.base import KeySetAll, KeySetAllExceptSome, KeySetNone, KeySetSome

print('Executed from command line...')
print(f'all: {KeySetAll()}')
print(f'none: {KeySetNone()}')
print(f'some: {KeySetSome(["A", "B"])}')
print(f'all except some: {KeySetAllExceptSome(["A", "B"])}')
