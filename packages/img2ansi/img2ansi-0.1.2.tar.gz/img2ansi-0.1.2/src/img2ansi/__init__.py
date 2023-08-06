# read version from installed package
from importlib.metadata import version
__version__ = version(__name__)

from img2ansi.img2ascii import main
from img2ansi.img2braile import main
from img2ansi.img2block import main
