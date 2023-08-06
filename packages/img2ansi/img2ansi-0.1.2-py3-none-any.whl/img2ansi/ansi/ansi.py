"""ANSI Escape Sequence

This scripts allows to use the ansi sequences
with ease, in particular allows for a custom sequences
for any length character sequence

"""

from enum import IntFlag

class Ansi(IntFlag):
    """ Class defining ANSI Escape Sequence flags

    This class allow the use of
    ANSI Sequence codes as bitwise flags

    """

    NONE = (1 << 0)
    RESET = (1 << 1)
    BOLD = (1 << 2)
    BLINK = (1 << 3)
    FRGD = (1 << 4)
    BKGD = (1 << 5)

def get_ansi_seq(ANSIMODE, rgb=(0xff, 0xff, 0xff)):
    """
    Get the corresponding ANSI sequence

    Parameters
    ----------
    ANSIMODE : int
        The ansi sequence to perform
    rgb : tupple
        A tupple containing the RGB components used for background
        or foreground sequence

    Returns
    -------
    str
        a str containing the ansi sequence and if required
        the color parameters
    """
    ansiSeq = ""
    if(Ansi.NONE & ANSIMODE):
        return ansiSeq
    else:
        if(Ansi.RESET & ANSIMODE):
            ansiSeq += "\033[m"
        if(Ansi.BOLD & ANSIMODE):
            ansiSeq += "\033[1m"
        if(Ansi.BLINK & ANSIMODE):
            ansiSeq += "\033[5m"
        if(Ansi.FRGD & ANSIMODE):
            ansiSeq += "\033[38;2;{};{};{}m".format(rgb[0], rgb[1], rgb[2])
        if(Ansi.BKGD & ANSIMODE):
            ansiSeq += "\033[48;2;{};{};{}m".format(rgb[0], rgb[1], rgb[2])

    return ansiSeq
