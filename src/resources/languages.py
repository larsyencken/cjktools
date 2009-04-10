# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# languages.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 26 14:11:21 2006
#
#----------------------------------------------------------------------------#

"""
A list of common languages and character codes.
"""

#----------------------------------------------------------------------------#

import os, sys

from cjktools.maps import invert_injective_mapping

#----------------------------------------------------------------------------#

to_one_char_code = {
            'English':      'e',
            'Chinese':      'c',
            'Japanese':     'j',
            'German':       'g',
            'French':       'f',
            'Spanish':      's',
            'Portugese':    'p',
        }

from_one_char_code = invert_injective_mapping(to_one_char_code)

#----------------------------------------------------------------------------#

to_two_char_code = {
            'English':      'en',
            'Chinese':      'cn',
            'Japanese':     'jp',
        }

from_two_char_code = invert_injective_mapping(to_two_char_code)

#----------------------------------------------------------------------------#

