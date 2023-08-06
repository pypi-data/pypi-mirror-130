#!/usr/bin/env python3
"""
This script defines the img2block CLI parameters,
and calls the according classes to perform the task
"""

import sys
import argparse
from img2ansi.block.block import *


def create_parser(args):
    """Creates an argument parser for the img2block CLI

    Returns
    -------
    argparse
        a set of args to perform specified convertion
    """

    # Setup parser
    parser = argparse.ArgumentParser(
        description="Convert img to Block representation",
        epilog="""By default uses 2 blocks per terminal cell
                and -r 0 0 """,
    )

    parser.add_argument('-f', '--fullscreen',
                        action='store_true', help='fullscreen flag',
                        default=False)

    parser.add_argument('-W', '--wholeblock',
                        action='store_true',
                        help=""""Use one block per terminal cell""",
                        default=False)

    parser.add_argument('-k', '--blink',
                        action='store_true', help='blink flag',
                        default=False)

    parser.add_argument('-n', '--noecho',
                        action='store_true', help="no echo flag",
                        default=False)

    parser.add_argument('-r', '--resize', metavar=("Width", "Height"),
                        nargs=2, type=int,
                        help="""resize image (0 0 keeps original size),
                        if given -r 100 0 keeps aspectratio with
                        100px width""",
                        default=[0, 0])

    parser.add_argument('-o', '--save', metavar="output filename",
                        nargs='?', type=str,
                        help="""save file""",
                        default="")

    parser.add_argument('inputImage', type=str,
                        help='image to be converted'
                        )

    return parser.parse_args(args)

def main(argv=None):
    """
    Handles all the program parameters and
    calls to perform the convertion

    Parameter
    ---------
    argv : list
        A list of parameters

    Returns
    -------
    str
        The result of convertion or empty str
    """

    # Create parser
    if( argv is None ):
        args = create_parser(sys.argv[1:])
    else:
        args = create_parser(argv)
    # Create instance
    converter = Block()
    # ** Handle all parameters **
    img = Image.open(args.inputImage)
    # Setup ansimode
    ansimode = Ansi.NONE
    # Unset None if any ansi sequence is used
    if(args.blink):
        ansimode &= ~Ansi.NONE
        ansimode |= Ansi.BLINK
    # Resize if necessary
    if(args.resize != [0,0]):
        img = converter.resize(img, *args.resize,
                         args.fullscreen,
                         args.wholeblock)
    # Call convert method
    result = converter.convert(img, ansimode,
                               args.wholeblock)
    # Save to file
    if (args.save != ""):
        converter.save(args.save)
    # if echo return result
    if(args.noecho == False):
        return result
    # return empty string
    return ""
