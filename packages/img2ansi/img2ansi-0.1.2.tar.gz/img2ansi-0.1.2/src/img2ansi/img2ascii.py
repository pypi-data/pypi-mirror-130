#!/usr/bin/env python3
"""
This script defines the img2ascii CLI parameters,
and calls the according classes to perform the task
"""

import sys
import argparse
from img2ansi.ascii.ascii import *


def create_parser(args):
    """Creates an argument parser for the img2ascii CLI

    Returns
    -------
    argparse
        a set of args to perform specified convertion
    """

    # Setup parser
    parser = argparse.ArgumentParser(
        description="Convert img to Ascii representation",
        epilog="""By default uses parameters -r 0 0 -a " .~*:+zM#&@$" """
    )

    parser.add_argument('-a', '--asciicharset', metavar="Character Set",
                        type=str,
                        help="""ascii character set (default :
                        " .~*:+zM#&@$" )""",
                        default="")

    parser.add_argument('-F', '--frgdcolor', metavar=("R", "G", "B"),
                        nargs=3, type=lambda x: int(x,0),
                        help="""All characters with RGB24 foreground color""",
                        default=[])

    parser.add_argument('-B', '--bkgdcolor', metavar=("R", "G", "B"),
                        nargs=3, type=lambda x: int(x,0),
                        help="""All characters with RGB24 background color""",
                        default=[])

    parser.add_argument('-b', '--bold',
                        action='store_true', help='bold flag',
                        default=False)

    parser.add_argument('-c', '--color',
                        action='store_true', help='foreground text as img colors',
                        default=False)

    parser.add_argument('-f', '--fullscreen',
                        action='store_true', help='fullscreen flag',
                        default=False)

    parser.add_argument('-i', '--invertPattern',
                        action='store_true',
                        help=""""invert ascii character set""",
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
    converter = Ascii()
    # ** Handle all parameters **
    # Open the img
    img = Image.open(args.inputImage)
    # Setup ansimode
    ansimode = Ansi.NONE
    # Unset None if any ansi sequence is used
    if(args.bold or args.blink or args.color):
        ansimode &= ~Ansi.NONE
        if (args.bold):
            ansimode |= Ansi.BOLD
        if (args.blink):
            ansimode |= Ansi.BLINK
        if (args.color):
            ansimode |= Ansi.FRGD
    # Resize if necessary
    if(args.resize != [0,0]):
        img = converter.resize(img, *args.resize,
                         args.fullscreen)
    # Change character set if necessary
    if(args.asciicharset != ""):
        converter.set_charset(args.asciicharset)
    # Perform convertion
    if(args.frgdcolor != [] or args.bkgdcolor != []):
        result = converter.convert(
                img, ansimode, args.invertPattern,
                args.frgdcolor != [], args.frgdcolor,
                args.bkgdcolor != [], args.bkgdcolor,
                )
    else:
        result = converter.convert(img, ansimode,
                                   args.invertPattern)
    # Save to file 
    if(args.save != ""):
        converter.save(args.save)
    # if echo return result
    if(args.noecho == False):
        return result
    # return empty string
    return ""

