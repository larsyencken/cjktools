# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# shellColor.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue May  2 11:36:56 2006
#
#----------------------------------------------------------------------------#

"""
Colored output for unix shells, which can be disabled to avoid problems on
non-supporting platforms.
"""

#----------------------------------------------------------------------------#

# whether color output is currently enabled or not
_enableColor = True

#----------------------------------------------------------------------------#

def enableColor():
    """Enable colorized output from this module's methods."""
    global _enableColor
    _enableColor = True
    return

#----------------------------------------------------------------------------#

def disableColor():
    """Disable colorized output from this module's methods."""
    global _enableColor
    _enableColor = False
    return

#----------------------------------------------------------------------------#

_colString = '\x1b[01;%.2dm'
_resetString = '\x1b[01;00m'

colors = {
    'regular':      0,
    'darkgrey':     30,
    'red':          31,
    'lightgreen':   32,
    'yellow':       33,
    'blue':         34
    }

#----------------------------------------------------------------------------#

def color(strObj, color):
    """
    Changes the color of the given string as printed on a UNIX shell.
    
    The returned string contains escape sequences which
    """ 
    global _enableColor
    if _enableColor:
        return (_colString % colors[color]) + strObj + (_colString % 0)
    else:
        return strObj

#----------------------------------------------------------------------------#

def changeColor(color):
    """ Change the color for the remaining text after this is printed to the
        given color.
    """
    global _enableColor
    if _enableColor:
        return _colString % colors[color]
    else:
        return ''

#----------------------------------------------------------------------------#

def realLen(strObj):
    """
    Determine the real length of a string object.
    """
    finalLen = 0
    startIndex = 0

    colorStr = '\x1b[01;'

    nextColor = strObj.find(colorStr, startIndex)
    while nextColor != -1:
        finalLen += nextColor - startIndex
        startIndex = nextColor + len(_resetString)
        nextColor = strObj.find(colorStr, startIndex)

    finalLen += len(strObj) - startIndex

    return finalLen

#----------------------------------------------------------------------------#

def resetColor():
    """
    Return the string to print to reset the color to the default.
    """
    global _enableColor

    if _enableColor:
        return _resetString

    return ''

#----------------------------------------------------------------------------#
