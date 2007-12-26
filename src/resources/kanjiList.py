# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# kanjiList.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 12 19:18:19 2006
#
#----------------------------------------------------------------------------#

"""
An interface to the kanji lists.
"""

#----------------------------------------------------------------------------#

import os
import settings
from cjktools.common import sopen
from cjktools import scripts

#----------------------------------------------------------------------------#

_kanjiListDir = os.path.join(settings.DATA_DIR, 'kanji-lists')

#----------------------------------------------------------------------------#

def getLists():
    """
    Returns list containing the names of all existing kanji lists.
    """
    global _kanjiListDir
    result = []
    for filename in os.listdir(_kanjiListDir):
        result.append(os.path.splitext(filename)[0])

    return result

#----------------------------------------------------------------------------#

def getList(listName):
    """
    Returns the kanji in the given list.
    """
    iStream = sopen(os.path.join(_kanjiListDir, '%s.list' % listName))
    data = iStream.read()
    iStream.close()

    return scripts.uniqueKanji(data)

#----------------------------------------------------------------------------#
