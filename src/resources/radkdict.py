#!/usr/bin/env python
#----------------------------------------------------------------------------#
# radkdict.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue May  2 15:44:24 2006
#
#----------------------------------------------------------------------------#

"""
Based on the radkfile, a dictionary mapping character to bag of radicals.
"""

#----------------------------------------------------------------------------#

from cjktools import maps
from cjktools.common import sopen

import settings

from os import path
import sys

#----------------------------------------------------------------------------#

_defaultFile = path.join(settings.DATA_DIR, 'radkfile')

#----------------------------------------------------------------------------#

class RadkDict(dict):
    """
    Determines which radicals a character contains.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, dictFile=_defaultFile):
        """
        Constructor.
        
        @param dictFile: The radkfile to parse.
        """
        self._parseRadkfile(dictFile)
        return

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#

    def _parseRadkfile(self, filename):
        """
        Parses the radkfile and populates the current dictionary.
        
        @param filename: The radkfile to parse.
        """
        radicalToKanji = {}
        radicalToStrokeCount = {}

        currentRadical = None
        strokeCount = None

        for line in sopen(filename, 'r', 'utf8'):
            if line.startswith('#'):
                # found a comment line
                continue

            if line.startswith('$'):
                # found a line with a new radical
                dollar, currentRadical, strokeCount = line.split()
                radicalToStrokeCount[currentRadical] = int(strokeCount)
                continue

            # found a line of kanji
            kanji = line.strip()
            radicalToKanji.setdefault(currentRadical, []).extend(kanji)

        self.update(maps.invertMapping(radicalToKanji))
        maps.mapDict(tuple, self, inPlace=True)

        self.radicalToStrokeCount = radicalToStrokeCount
        self.radicalToKanji = radicalToKanji

        return

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

_radicalDict = None

def getRadkDict():
    """
    Fetches a new copy of the radical dictionary.
    """
    global _radicalDict
    if _radicalDict is None:
        _radicalDict = RadkDict()

    return _radicalDict

#----------------------------------------------------------------------------#

def printRadicals(kanjiList):
    """
    Print out each kanji and the radicals it contains.
    """
    radicalDict = RadkDict()
    for kanji in kanjiList:
        kanji = unicode(kanji, 'utf8')
        radicals = radicalDict[kanji]

        print '%s: ' % kanji, ' '.join(sorted(radicals))

    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    printRadicals(sys.argv[1:])

