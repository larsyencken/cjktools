# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# pinyinTable.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 12 12:00:21 2006
#----------------------------------------------------------------------------#

"""
A table for conversion of hanzi to pinyin.
"""

#----------------------------------------------------------------------------#

import re
import codecs
import pkg_resources

import zhuyinTable

#----------------------------------------------------------------------------#
# PUBLIC
#----------------------------------------------------------------------------#

vowels = u'aeiouü'
consonants = u'bcdfghjklmnpqrstvwxyz'
toneToVowels = {
            0: u'aeiouü',
            1: u'āēīōūǖ',
            2: u'áéíóúǘ',
            3: u'ǎěǐǒǔǚ',
            4: u'àèìòùǜ',
        }

_cachedPinyinTable = None
_cachedPinyinSegmenter = None

#----------------------------------------------------------------------------#

class PinyinFormatError(Exception):
    pass

#----------------------------------------------------------------------------#

class PinyinTable(dict):
    """
    A reader which converts Chinese hanzi to pinyin.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self):
        """Constructor."""
        self._segmenter = getPinyinSegmenter()

        # Load the table mapping hanzi to pinyin.
        iStream = codecs.getreader('utf8')(
                pkg_resources.resource_stream('cjktools_data',
                'tables/gbk_pinyin_table')
            )
        for line in iStream:
            if line.startswith('#'):
                continue
            entries = line.rstrip().split()
            hanzi = entries[0]
            numericReadings = tuple(entries[1:])
            self[hanzi] = tuple(numericReadings)
        iStream.close()

        return

    #------------------------------------------------------------------------#

    def fromHanzi(self, hanziString, inline=True, useTones=True):
        """Convert all the hanzi in the given string to pinyin readings."""
        if not useTones:
            inline = False

        result = []
        for char in hanziString:
            numericReading = self.get(char, (char,))[0]

            if inline:
                result.append(self.fromAscii(numericReading))
            elif not useTones:
                result.append(self.stripTones(numericReading))
            else:
                result.append(numericReading)

        return ''.join(result)

    #------------------------------------------------------------------------#

    def fromAscii(self, asciiPinyin):
        """
        Takes a string in ascii pinyin style, e.g. "li1bao2" and turns it
        into unicode pinyin.
        """
        standardForm = normalize(asciiPinyin)
        chunks = self._segmenter.segmentPinyin(standardForm)

        chunks = [self._applyTone(p, t) for (p, t) in chunks]
        return ''.join(chunks)
    
    #------------------------------------------------------------------------#

    def stripTones(self, asciiPinyin):
        """
        Return the same ascii pinyin string, but without any tones.
        """
        standardForm = normalize(asciiPinyin)
        chunks = self._segmenter.segmentPinyin(standardForm)
        return ''.join(p for (p, t) in chunks)

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#
    
    def _applyTone(self, syllable, tone):
        """
        Apply a tone to a syllable.
        """
        if tone == 5:
            tone = 0
        results = []
        results.append(syllable[0])
        
        usedTone = False
        for char in syllable[1:]:
            if not usedTone and char in vowels:
                results.append(toneToVowels[tone][vowels.index(char)])
                usedTone = True
            else:
                results.append(char)

        return ''.join(results)

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

class PinyinSegmenter(object):
    """
    Create an object which can segment pinyin.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self):
        """
        Constructor.
        """
        #self.wildCard = UNKNOWN_WILDCARD
        self.replacement = '#'

        basePattern = '(%s|%s)' % (
                zhuyinTable.pinyinRegexPattern(),
                self.replacement,
            )
        self.singlePattern = re.compile(basePattern, re.UNICODE)
        self.stringPattern = re.compile('(%s)+' % basePattern, re.UNICODE)
        return

    #------------------------------------------------------------------------#

    def segmentPinyin(self, pinyinString):
        """
        Segment the given pinyin string.
        """
        #pinyinString = pinyinString.replace(self.wildCard, self.replacement)
        pinyinString = normalize(pinyinString)
        result = self.singlePattern.findall(pinyinString)
        corrected = []
        for block, pinyin, tone in result:
#            # When the wildcard replacement is found, it will only fill the
#            # block.
#            if block == self.replacement:
#                pinyin = self.wildCard

            # Tone defaults to neutral tone.
            if tone == '':
                tone = 0
            else:
                tone = int(tone)

            # Handle special case of 儿 shortening from "er" to "r".
            if pinyin == 'r':
                pinyin = 'er'

            corrected.append((pinyin, tone))

        return tuple(corrected)

    #------------------------------------------------------------------------#

    def isPinyin(self, symbolString):
        """
        Returns True if the symbol string matches.
        """
        return bool(self.stringPattern.match(normalize(symbolString)))

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#
    
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

def normalize(asciiPinyin):
    """
    Normalises a pinyin string.
    """
    normalVersion = asciiPinyin.lower().replace(' ', '')
    normalVersion = normalVersion.replace(u'v', u'ü')

    return normalVersion

#----------------------------------------------------------------------------#

def getPinyinTable():
    """
    Constructs a pinyin table object, or fetches a cached one.
    """
    global _cachedPinyinTable

    if _cachedPinyinTable is None:
        _cachedPinyinTable = PinyinTable()

    return _cachedPinyinTable

#----------------------------------------------------------------------------#

def getPinyinSegmenter():
    """
    Fetches a cached pinyin segmenter.
    """
    global _cachedPinyinSegmenter

    if _cachedPinyinSegmenter is None:
        # Cache miss, create a new object.
        _cachedPinyinSegmenter = PinyinSegmenter()

    return _cachedPinyinSegmenter

#----------------------------------------------------------------------------#
