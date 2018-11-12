#!/usr/bin/env python
"""
Plot a functional group, one plot per bond in the database.
"""

from argparse import ArgumentParser

from rascall import database

if __name__ == '__main__':
    PARSER = ArgumentParser(description=__doc__)
    PARSER.add_argument("fg", nargs="?", help="Functional Group to Plot", default="[!#1]C#C[!#1]")

    args = PARSER.parse_args()

    database.plot(args.fg)
