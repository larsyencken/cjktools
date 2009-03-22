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
        '/opt/local/share/cjktools-data',
        # Add an explicit directory where data files are stored here.
    ]


_cachedDataDir = os.environ.get('CJKTOOLS_DATA_DIR', None)

def getDataDir():
    global _cachedDataDir
    if _cachedDataDir is None:
        for candidate in _candidates:
            if os.path.isdir(candidate):
                _cachedDataDir = candidate
                break
    
    if _cachedDataDir is None:
        raise Exception('no default data directory found -- set CJKTOOLS_DATA_DIR environment variable')
    
    return _cachedDataDir

#----------------------------------------------------------------------------#
