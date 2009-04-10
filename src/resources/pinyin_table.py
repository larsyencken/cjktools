# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# pinyin_table.py
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

import zhuyin_table

#----------------------------------------------------------------------------#
# PUBLIC
#----------------------------------------------------------------------------#

vowels = u'aeiouü'
consonants = u'bcdfghjklmnpqrstvwxyz'
tone_to_vowels = {
            0: u'aeiouü',
            1: u'āēīōūǖ',
            2: u'áéíóúǘ',
            3: u'ǎěǐǒǔǚ',
            4: u'àèìòùǜ',
        }

_cached_pinyin_table = None
_cached_pinyin_segmenter = None

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
        self._segmenter = get_pinyin_segmenter()

        # Load the table mapping hanzi to pinyin.
        i_stream = codecs.getreader('utf8')(
                pkg_resources.resource_stream('cjktools_data',
                'tables/gbk_pinyin_table')
            )
        for line in i_stream:
            if line.startswith('#'):
                continue
            entries = line.rstrip().split()
            hanzi = entries[0]
            numeric_readings = tuple(entries[1:])
            self[hanzi] = tuple(numeric_readings)
        i_stream.close()

        return

    #------------------------------------------------------------------------#

    def from_hanzi(self, hanzi_string, inline=True, use_tones=True):
        """Convert all the hanzi in the given string to pinyin readings."""
        if not use_tones:
            inline = False

        result = []
        for char in hanzi_string:
            numeric_reading = self.get(char, (char,))[0]

            if inline:
                result.append(self.from_ascii(numeric_reading))
            elif not use_tones:
                result.append(self.strip_tones(numeric_reading))
            else:
                result.append(numeric_reading)

        return ''.join(result)

    #------------------------------------------------------------------------#

    def from_ascii(self, ascii_pinyin):
        """
        Takes a string in ascii pinyin style, e.g. "li1bao2" and turns it
        into unicode pinyin.
        """
        standard_form = normalize(ascii_pinyin)
        chunks = self._segmenter.segment_pinyin(standard_form)

        chunks = [self._apply_tone(p, t) for (p, t) in chunks]
        return ''.join(chunks)
    
    #------------------------------------------------------------------------#

    def strip_tones(self, ascii_pinyin):
        """
        Return the same ascii pinyin string, but without any tones.
        """
        standard_form = normalize(ascii_pinyin)
        chunks = self._segmenter.segment_pinyin(standard_form)
        return ''.join(p for (p, t) in chunks)

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#
    
    def _apply_tone(self, syllable, tone):
        """
        Apply a tone to a syllable.
        """
        if tone == 5:
            tone = 0
        results = []
        results.append(syllable[0])
        
        used_tone = False
        for char in syllable[1:]:
            if not used_tone and char in vowels:
                results.append(tone_to_vowels[tone][vowels.index(char)])
                used_tone = True
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
        #self.wild_card = UNKNOWN_WILDCARD
        self.replacement = '#'

        base_pattern = '(%s|%s)' % (
                zhuyin_table.pinyin_regex_pattern(),
                self.replacement,
            )
        self.single_pattern = re.compile(base_pattern, re.UNICODE)
        self.string_pattern = re.compile('(%s)+' % base_pattern, re.UNICODE)
        return

    #------------------------------------------------------------------------#

    def segment_pinyin(self, pinyin_string):
        """
        Segment the given pinyin string.
        """
        #pinyin_string = pinyin_string.replace(self.wild_card, self.replacement)
        pinyin_string = normalize(pinyin_string)
        result = self.single_pattern.findall(pinyin_string)
        corrected = []
        for block, pinyin, tone in result:
#            # When the wildcard replacement is found, it will only fill the
#            # block.
#            if block == self.replacement:
#                pinyin = self.wild_card

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

    def is_pinyin(self, symbol_string):
        """
        Returns True if the symbol string matches.
        """
        return bool(self.string_pattern.match(normalize(symbol_string)))

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#
    
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

def normalize(ascii_pinyin):
    """
    Normalises a pinyin string.
    """
    normal_version = ascii_pinyin.lower().replace(' ', '')
    normal_version = normal_version.replace(u'v', u'ü')

    return normal_version

#----------------------------------------------------------------------------#

def get_pinyin_table():
    """
    Constructs a pinyin table object, or fetches a cached one.
    """
    global _cached_pinyin_table

    if _cached_pinyin_table is None:
        _cached_pinyin_table = PinyinTable()

    return _cached_pinyin_table

#----------------------------------------------------------------------------#

def get_pinyin_segmenter():
    """
    Fetches a cached pinyin segmenter.
    """
    global _cached_pinyin_segmenter

    if _cached_pinyin_segmenter is None:
        # Cache miss, create a new object.
        _cached_pinyin_segmenter = PinyinSegmenter()

    return _cached_pinyin_segmenter

#----------------------------------------------------------------------------#
