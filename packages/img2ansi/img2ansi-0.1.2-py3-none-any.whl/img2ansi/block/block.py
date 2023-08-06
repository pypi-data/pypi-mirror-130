"""
This script defines a class to convert an image to
a unicode block representation, which allows to
preview an approximation of the image on the terminal

"""

from PIL import Image
from os import get_terminal_size
from img2ansi.ansi.ansi import *

class Block():
    """
    Convert a PIL (img) to a block representation
    basically show the actual image with a lower
    resolution to fit in terminal screen

    Attributes
    ----------
    blockRepr : list
        A list with all the convertion data
    blockChar : str
        Unicode str of upper square solid block

    """

    def __init__(self):
        """
        Initialize all attributes
        """

        self.blockRepr = ""
        # Upper half block
        self.blockChar = "\u2580"
        # Lower half block
        #self.blockChar = "\u2584"

    def print(self):
        """
        Print representation to terminal
        """

        print(self.blockRepr)

    def save(self, filename):
        """
        Save representation to a file
        """

        with open(filename, "w") as f:
            f.write(self.blockRepr)

    def convert(self, img, ansimode=Ansi.NONE, wholeblock=False):
        """
        Convert PIL (img) to unicode block representation
        """


        if(wholeblock):
            self.convert_wholeblock(img, ansimode)
        else:
            self.convert_halfblock(img, ansimode)

        return self.blockRepr

    def convert_wholeblock(self, img, ansimode):
        """
        Convertion assign each block per terminal cell
        """

        # Reset representation
        self.blockRepr = ""
        # Convert img to RGB
        rgbimg = img.convert("RGB")
        # Get img dimensions
        width = img.width
        height = img.height
        #
        for y in range(0, height):
            # Add optional ansi (just blink can be applied)
            self.blockRepr += get_ansi_seq(ansimode & ~
                                            Ansi.BKGD & ~
                                            Ansi.FRGD)
            for x in range(0, width):
                # Add bkgdcolor
                pixel = rgbimg.getpixel((x,y))
                self.blockRepr += get_ansi_seq(Ansi.BKGD,
                                               pixel)
                # Add empty space
                self.blockRepr += " "
            self.blockRepr += get_ansi_seq(Ansi.RESET)
            self.blockRepr += "\n"


    def convert_halfblock(self, img, ansimode):
        """
        Convertion assign two blocks per terminal cell
        """
        # Convert img to RGB
        rgbimg = img.convert("RGB")
        # Get img dimensions
        width = img.width
        height = img.height
        # Iterate through image in 1x2 window
        # Ignore at most 1 row 
        # Need to get default background of terminal
        # To add last row, but i'm lazy and dont know
        # how to do it without importing curses
        for y in range(0, height - (height % 2), 2):
            # Add optional ansi
            # This convertion mode doesn't support custom
            # background or foreground color since are already used
            # to color the blocks themselves
            self.blockRepr += get_ansi_seq(ansimode & ~
                                            Ansi.BKGD & ~
                                            Ansi.FRGD)
            for x in range(0, width):
                # Get RGB pixel values
                RGBupper = rgbimg.getpixel((x, y))
                RGBlower = rgbimg.getpixel((x, y + 1))
                # Set foreground to actual block char (upper block)
                self.blockRepr += get_ansi_seq( Ansi.FRGD,
                                               RGBupper)
                # Set background to simulate block
                self.blockRepr += get_ansi_seq( Ansi.BKGD,
                                               RGBlower)
                self.blockRepr += self.blockChar
            # Add newline char at each row end
            self.blockRepr += get_ansi_seq(Ansi.RESET)
            self.blockRepr += "\n"

    def resize(self, img, width, height, fullscreen, wholeblock):
        """
        Resize img according to width, height and fullscreen
        To perform resampling the LANCZOS algorithm is used.

        """
        if(fullscreen):
            # Resize to fullscreen -Fr 0 0
            if(width == 0 and height == 0):
                w, h = get_terminal_size()
                if(wholeblock):
                    rimg = img.resize((w, h),
                                            Image.LANCZOS)
                else:
                    rimg = img.resize((w, 2 * h),
                                            Image.LANCZOS)
            # Keep aspect ratio, height -> terminal height -F -r 0 y
            elif(width == 0 and height != 0):
                AspectRatio = img.width / img.height
                _, h = get_terminal_size()
                if(wholeblock):
                    rimg = img.resize(
                        (int(h * AspectRatio), h), Image.LANCZOS)
                else:
                    rimg = img.resize(
                        (int(1 * h * AspectRatio), 2 * h), Image.LANCZOS)
            # Keep aspect ratio, width -> terminal width -Fr x 0
            elif(width != 0 and height == 0):
                AspectRatio = img.height / img.width
                w, _ = get_terminal_size()
                if(wholeblock):
                    rimg = img.resize(
                        (w, int(w * AspectRatio)), Image.LANCZOS)
                else:
                    rimg = img.resize(
                        (1 * w, int(2 * w * AspectRatio)), Image.LANCZOS)
            # Resize to given size -Fr x y.
            elif(width != 0 and height != 0):
                if(wholeblock):
                    rimg = img.resize(
                        (width, height),
                        Image.LANCZOS)
                else:
                    rimg = img.resize(
                        (1 * width, 2 * height),
                        Image.LANCZOS)
        else:
            # Resize to given size -r x y
            if(width != 0 and height != 0):
                if(wholeblock):
                    rimg = img.resize(
                        (2 * width, height),
                        Image.LANCZOS)
                else:
                    rimg = img.resize(
                        (1 * width, 2 * height),
                        Image.LANCZOS)
            # Keep aspect ratio, height -> resizeheight -r 0 y
            elif(width == 0 and height != 0):
                AspectRatio = img.width / img.height
                if(wholeblock):
                    rimg = img.resize(
                        (int(2 * height * AspectRatio),
                         height), Image.LANCZOS)
                else:
                    rimg = img.resize(
                        (int(2 * height * AspectRatio),
                         2 * height), Image.LANCZOS)
            # Keep aspect ratio, width -> resizewidth -r x 0
            elif(width != 0 and height == 0):
                AspectRatio = img.height / img.width
                if(wholeblock):
                    rimg = img.resize((width,
                        int(2 * width * AspectRatio)),
                        Image.LANCZOS)
                else:
                    rimg = img.resize((2 * width,
                        int(2 * width * AspectRatio)),
                        Image.LANCZOS)

        return rimg

