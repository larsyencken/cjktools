# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# kanjidic.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Fri Apr 28 16:09:09 2006
#
#----------------------------------------------------------------------------#

"""
A nice interface to the Kanjidic dictionary.
"""

#----------------------------------------------------------------------------#

from cjktools.common import smartLineIter
from cjktools import scripts

import settings

import re
from os import path

#----------------------------------------------------------------------------#

def getDefaultFiles():
    return [
        path.join(settings.getDataDir(), 'kanjidic'),
        path.join(settings.getDataDir(), 'kanjd212')
    ]

#----------------------------------------------------------------------------#

basicFeatures = set([
        'gloss',
        'strokeCount',
        'jyouyouGrade',
        'skipCode',
        'onyomi',
        'kunyomi',
        'unicode'
    ])

#----------------------------------------------------------------------------#

remappings = {
        'B':    'radicalIndex',
        'C':    'classicalRadicalIndex',
        'F':    'frequency',
        'G':    'jyouyouGrade',
        'H':    'halpernIndex',
        'N':    'nelsonIndex',
        'V':    'newNelsonIndex',
        'D':    'dictionaryCode',
        'P':    'skipCode',
        'S':    'strokeCount',
        'U':    'unicode',
        'I':    'spahnCode',
        'Q':    'fourCornerCode',
        'M':    'morohashiIndex',
        'E':    'henshallCode',
        'K':    'gakkenCode',
        'L':    'heisigCode',
        'O':    'oneillCode',
        'W':    'koreanReading',
        'Y':    'pinyinReading',
        'X':    'crossReferences',
        'Z':    'misclassifiedAs'
    }

#----------------------------------------------------------------------------#

class KanjidicEntry:
    """
    A single entry in the kanjidic file.
    """
    #------------------------------------------------------------------------#

    def __init__(self, entryDetails):
        assert 'onReadings' in entryDetails and 'kunReadings' in entryDetails
        self.__dict__.update(entryDetails)
        return

    #------------------------------------------------------------------------#

    def getAllReadings(self):
        """
        Construct a reading pool for this entry.
        """
        readingSet = set()
        for reading in self.kunReadings + \
                    map(scripts.toHiragana, self.onReadings):
            # Ignore suffix/prefix information about readings.
            if '-' in reading:
                reading = reading.replace('-', '')

            # Only use the stem  of okurigana readings.
            if '.' in reading:
                stem, suffix = reading.split('.')
                reading = stem

            readingSet.add(reading)

        return readingSet

    allReadings = property(getAllReadings)

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

class Kanjidic(dict):
    """
    An interface to the kanjidic dictionary. Create a new instance to parse
    the dictionary. Has a nice getitem interface to get the details of a
    character.
    """

    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, kanjidicFiles=None):
        """
        Constructor.

        @param kanjidicFiles: The files corresponding to kanjidic.
        """
        dict.__init__(self)

        if kanjidicFiles is None:
            kanjidicFiles = getDefaultFiles()

        self._parseKanjidic(kanjidicFiles)

        return

    #------------------------------------------------------------------------#

    @classmethod
    def getCached(cls):
        if not hasattr(cls, '_cached'):
            cls._cached = cls()

        return cls._cached

    #------------------------------------------------------------------------#
    # PRIVATE
    #------------------------------------------------------------------------#

    def _parseKanjidic(self, files):
        """
        Parses the kanjidic file for its contents, updating this class
        with a kanji -> info mapping.

        @param files: The files for kanjidic.
        """
        self._dictionary = {}

        for line in smartLineIter(files):
            if line.startswith('#'):
                continue

            entry = self._parseLine(line)
            self.__setitem__(entry.kanji, entry)

        return

    #------------------------------------------------------------------------#

    def _parseLine(self, line):
        """
        Parses a single line in the kanjdic file, returning an entry.
        """
        segmentPattern = re.compile('[^ {]+|{.*?}', re.UNICODE)
        segments = segmentPattern.findall(line.strip())

        kanji = segments[0]
        jisCode = int(segments[1], 16)
        kanjiInfo = {
                'kanji':        kanji,
                'gloss':        [],
                'onReadings':   [],
                'kunReadings':  [],
                'jisCode':      jisCode
            }

        i = 2
        numSegments = len(segments)
        while i < numSegments:
            thisSegment = segments[i]
            i += 1

            if thisSegment.startswith('{'):
                # It's a gloss.
                kanjiInfo['gloss'].append(thisSegment[1:-1])

            elif (scripts.scriptType(thisSegment) != scripts.Script.Ascii 
                    or thisSegment.startswith('-')):
                # It must be a reading.
                char = thisSegment[0]
                if char == '-':
                    char = thisSegment[1]

                if scripts.scriptType(char) == scripts.Script.Katakana:
                    kanjiInfo['onReadings'].append(thisSegment)
                elif scripts.scriptType(char) == scripts.Script.Hiragana:
                    kanjiInfo['kunReadings'].append(thisSegment)
                else:
                    raise Exception, "Unknown segment %s" % thisSegment

            elif thisSegment in ('T1', 'T2'):
                continue

            else:
                # handle various codes
                code = thisSegment[0]
                remainder = thisSegment[1:]
                try:
                    remainder = int(remainder)
                except:
                    pass

                kanjiInfo.setdefault(remappings[code], []).append(
                    remainder)

        kanjiInfo['strokeCount'] = kanjiInfo['strokeCount'][0]
        if kanjiInfo.has_key('frequency'):
            kanjiInfo['frequency'] = int(kanjiInfo['frequency'][0])

        kanjiInfo['skipCode'] = tuple(map(
                int,
                kanjiInfo['skipCode'][0].split('-')
            ))

        kanjidicEntry = KanjidicEntry(kanjiInfo)

        return kanjidicEntry

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# PRIVATE
#----------------------------------------------------------------------------#

# An in-memory cached version.
_cachedKanjidic = None

#----------------------------------------------------------------------------#
