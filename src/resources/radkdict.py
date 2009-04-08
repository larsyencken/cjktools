#!/usr/bin/env python
#----------------------------------------------------------------------------#
# radkdict.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue May  2 15:44:24 2006
#
#----------------------------------------------------------------------------#

"Based on the radkfile, a dictionary mapping character to bag of radicals."

#----------------------------------------------------------------------------#

import codecs
import sys
import pkg_resources

from cjktools import maps
from cjktools.common import sopen

#----------------------------------------------------------------------------#

class RadkDict(dict):
    "Determines which radicals a character contains."
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, dict_file=None):
        """
        @param dictFile: The radkfile to parse.
        """
        if dict_file is None:
            line_stream = codecs.getreader('utf8')(
                    pkg_resources.resource_stream('cjktools_data', 'radkfile')
                )
        else:
            line_stream = sopen(dict_file)
            
        self._parse_radkfile(line_stream)
        return

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#

    def _parse_radkfile(self, line_stream):
        """
        Parses the radkfile and populates the current dictionary.
        
        @param filename: The radkfile to parse.
        """
        radicalToKanji = {}
        radicalToStrokeCount = {}

        currentRadical = None
        strokeCount = None

        for line in line_stream:
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

    @classmethod
    def getCached(cls):
        "Returns a memory-cached class instance."
        if not hasattr(cls, '_cached'):
            cls._cached = cls()

        return cls._cached

#----------------------------------------------------------------------------#

def printRadicals(kanjiList):
    "Print out each kanji and the radicals it contains."
    radicalDict = RadkDict()
    for kanji in kanjiList:
        kanji = unicode(kanji, 'utf8')
        radicals = radicalDict[kanji]

        print '%s: ' % kanji, ' '.join(sorted(radicals))

    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    printRadicals(sys.argv[1:])

