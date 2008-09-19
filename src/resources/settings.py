# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# settings.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Sat Oct 13 16:33:21 2007
#
#----------------------------------------------------------------------------#

"Settings for the cjktools.dict package."

#----------------------------------------------------------------------------#

import os

_candidates = [
        '/usr/share/cjktools-data',
        '/usr/local/share/cjktools-data',
    ]

DATA_DIR = None
for candidate in _candidates:
    if os.path.isdir(candidate):
        DATA_DIR = candidate
        break

#----------------------------------------------------------------------------#
