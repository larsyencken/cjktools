# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# shell_color.py
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
_enable_color = True

#----------------------------------------------------------------------------#

def enable_color():
    """Enable colorized output from this module's methods."""
    global _enable_color
    _enable_color = True
    return

#----------------------------------------------------------------------------#

def disable_color():
    """Disable colorized output from this module's methods."""
    global _enable_color
    _enable_color = False
    return

#----------------------------------------------------------------------------#

_col_string = '\x1b[01;%.2dm'
_reset_string = '\x1b[01;00m'

colors = {
    'regular':      0,
    'darkgrey':     30,
    'red':          31,
    'lightgreen':   32,
    'yellow':       33,
    'blue':         34
    }

#----------------------------------------------------------------------------#

def color(str_obj, color):
    """
    Changes the color of the given string as printed on a UNIX shell.
    
    The returned string contains escape sequences which
    """ 
    global _enable_color
    if _enable_color:
        return (_col_string % colors[color]) + str_obj + (_col_string % 0)
    else:
        return str_obj

#----------------------------------------------------------------------------#

def change_color(color):
    """ Change the color for the remaining text after this is printed to the
        given color.
    """
    global _enable_color
    if _enable_color:
        return _col_string % colors[color]
    else:
        return ''

#----------------------------------------------------------------------------#

def real_len(str_obj):
    """
    Determine the real length of a string object.
    """
    final_len = 0
    start_index = 0

    color_str = '\x1b[01;'

    next_color = str_obj.find(color_str, start_index)
    while next_color != -1:
        final_len += next_color - start_index
        start_index = next_color + len(_reset_string)
        next_color = str_obj.find(color_str, start_index)

    final_len += len(str_obj) - start_index

    return final_len

#----------------------------------------------------------------------------#

def reset_color():
    """
    Return the string to print to reset the color to the default.
    """
    global _enable_color

    if _enable_color:
        return _reset_string

    return ''

#----------------------------------------------------------------------------#
