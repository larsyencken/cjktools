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

from cjktools.maps import invertInjectiveMapping

#----------------------------------------------------------------------------#

toOneCharCode = {
            'English':      'e',
            'Chinese':      'c',
            'Japanese':     'j',
            'German':       'g',
            'French':       'f',
            'Spanish':      's',
            'Portugese':    'p',
        }

fromOneCharCode = invertInjectiveMapping(toOneCharCode)

#----------------------------------------------------------------------------#

toTwoCharCode = {
            'English':      'en',
            'Chinese':      'cn',
            'Japanese':     'jp',
        }

fromTwoCharCode = invertInjectiveMapping(toTwoCharCode)

#----------------------------------------------------------------------------#

