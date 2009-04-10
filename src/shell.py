# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# shell.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jan  8 18:03:12 2007
#
#----------------------------------------------------------------------------#

"""
Methods for working with the shell.
"""

#----------------------------------------------------------------------------#

import sys
import os

#----------------------------------------------------------------------------#

def set_screen_title(title):
    """
    Sets the title of a screen window using the given escape sequence.
    """
    if os.environ['TERM'] == 'screen':
        sys.stdout.write('k%s\\' % title)
        sys.stdout.flush()

    return

#----------------------------------------------------------------------------#

