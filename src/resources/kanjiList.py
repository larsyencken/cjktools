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

def getKanjiListDir():
    return os.path.join(settings.getDataDir(), 'lists', 'char')

#----------------------------------------------------------------------------#

def getLists():
    """
    Returns list containing the names of all existing kanji lists.
    """
    result = []
    for filename in os.listdir(getKanjiListDir()):
        result.append(os.path.splitext(filename)[0])

    return result

#----------------------------------------------------------------------------#

def getList(listName):
    """
    Returns the kanji in the given list.
    """
    iStream = sopen(os.path.join(getKanjiListDir(), '%s.list' % listName))
    data = iStream.read()
    iStream.close()

    return scripts.uniqueKanji(data)

#----------------------------------------------------------------------------#
