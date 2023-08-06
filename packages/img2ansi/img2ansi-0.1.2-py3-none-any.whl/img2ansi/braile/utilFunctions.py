"""
This script defines some useful function for the convertion / analysis
of an image to convert to unicode braile characters
"""

def windowing(img, px, py):
    '''
    Takes an image and performs a windowing of 2x4 starting at
    pos = (px, py) interpret as upper-left corner of window

    Parameters
    ----------
    img : Image
        PIL Image to analyze
    px : int
        x coordinate of image to start windowing
    py : int
        y coordinate of image to start windowing

    Returns
    -------
    list
        a list of the pixels integer values in the window
    '''
    # Get upper-left pos of pixel window
    WindowPixels = []
    for dy in range(0, 4):
        for dx in range(0, 2):
            WindowPixels.append(img.getpixel((px + dx, py + dy)))

    return WindowPixels


def get_dominant_color(WindowPixels):
    """
    Takes a list of pixel values and obtains the most common
    element in the list, in this case the dominant color

    Parameters
    ----------
    WindowPixels : list
        A list of pixel values

    Returns
    -------
    int
        the dominant pixel color in WindowPixels
    """
    return max(set(WindowPixels), key=WindowPixels.count)


def filter_window(WindowPixels, Filtertype, threshold=0x7f):
    """
    Performs a transformation to a list of pixels, according
    to the given Filtertype.

    Parameters
    ----------
    WindowPixels : list
        A list of pixel values
    Filtertype : str
        A srt specifying the filter to use
    threshold : int
        Threshold value that some filter required (binarize)

    Returns
    -------
    list
        A list with the filtered pixels
    """
    if (Filtertype == "Binarize"):
        # Compare to middle gray tone
        return [int(p > threshold) for p in WindowPixels]
    # elif (Filtertype == "Dominant"):
    #    # Get dominat pixel value of window
    #    dominantcolor = getDominantColor(WindowPixels)
    #    #Keep result as either 0 or 1
    #    return dominantcolor, [ int( p > threshold) for p in WindowPixels]

    else:
        raise ValueError("Not valid Filtertype")
