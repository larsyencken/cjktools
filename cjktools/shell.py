# -*- coding: utf-8 -*-
#
#  shell.py
#  cjktools
#

"""
Methods for working with the shell.
"""

import sys
import os


def set_screen_title(title):
    "Sets the title of a screen window using the given escape sequence."
    if os.environ['TERM'] == 'screen':
        sys.stdout.write('k%s\\' % title)
        sys.stdout.flush()
