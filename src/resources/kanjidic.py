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

import re
from os import path
from itertools import chain

from cjktools import scripts
from cjktools.common import sopen

#----------------------------------------------------------------------------#

basic_features = set([
        'gloss',
        'stroke_count',
        'jyouyou_grade',
        'skip_code',
        'onyomi',
        'kunyomi',
        'unicode'
    ])

#----------------------------------------------------------------------------#

remappings = {
        'B':    'radical_index',
        'C':    'classical_radical_index',
        'F':    'frequency',
        'G':    'jyouyou_grade',
        'H':    'halpern_index',
        'N':    'nelson_index',
        'V':    'new_nelson_index',
        'D':    'dictionary_code',
        'P':    'skip_code',
        'S':    'stroke_count',
        'U':    'unicode',
        'I':    'spahn_code',
        'Q':    'four_corner_code',
        'M':    'morohashi_index',
        'E':    'henshall_code',
        'K':    'gakken_code',
        'L':    'heisig_code',
        'O':    'oneill_code',
        'W':    'korean_reading',
        'Y':    'pinyin_reading',
        'X':    'cross_references',
        'Z':    'misclassified_as'
    }

#----------------------------------------------------------------------------#

class KanjidicEntry(object):
    """
    A single entry in the kanjidic file.
    """
    #------------------------------------------------------------------------#

    def __init__(self, entry_details):
        assert 'on_readings' in entry_details and 'kun_readings' in entry_details
        self.__dict__.update(entry_details)
        return

    #------------------------------------------------------------------------#

    def get_all_readings(self):
        """
        Construct a reading pool for this entry.
        """
        reading_set = set()
        for reading in self.kun_readings + \
                    map(scripts.to_hiragana, self.on_readings):
            # Ignore suffix/prefix information about readings.
            if '-' in reading:
                reading = reading.replace('-', '')

            # Only use the stem  of okurigana readings.
            if '.' in reading:
                stem, suffix = reading.split('.')
                reading = stem

            reading_set.add(reading)

        return reading_set

    all_readings = property(get_all_readings)

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

    def __init__(self, kanjidic_files=None):
        """
        Constructor.

        @param kanjidic_files: The files corresponding to kanjidic.
        """
        dict.__init__(self)

        if kanjidic_files is None:
            import cjktools_data
            line_stream = chain(
                    cjktools_data.open_file('kanjidic'),
                    cjktools_data.open_file('kanjd212'),
                )
        else:
            line_stream = reduce(chain, [sopen(f) for f in kanjidic_files])

        self._parse_kanjidic(line_stream)

        return

    #------------------------------------------------------------------------#

    @classmethod
    def get_cached(cls):
        if not hasattr(cls, '_cached'):
            cls._cached = cls()

        return cls._cached

    #------------------------------------------------------------------------#
    # PRIVATE
    #------------------------------------------------------------------------#

    def _parse_kanjidic(self, line_stream):
        """
        Parses the kanjidic file for its contents, updating this class
        with a kanji -> info mapping.

        @param files: The files for kanjidic.
        """
        self._dictionary = {}

        for line in line_stream:
            if line.startswith('#'):
                continue

            entry = self._parse_line(line)
            self.__setitem__(entry.kanji, entry)

        return

    #------------------------------------------------------------------------#

    def _parse_line(self, line):
        """
        Parses a single line in the kanjdic file, returning an entry.
        """
        segment_pattern = re.compile('[^ {]+|{.*?}', re.UNICODE)
        segments = segment_pattern.findall(line.strip())

        kanji = segments[0]
        jis_code = int(segments[1], 16)
        kanji_info = {
                'kanji':        kanji,
                'gloss':        [],
                'on_readings':   [],
                'kun_readings':  [],
                'jis_code':      jis_code
            }

        i = 2
        num_segments = len(segments)
        while i < num_segments:
            this_segment = segments[i]
            i += 1

            if this_segment.startswith('{'):
                # It's a gloss.
                kanji_info['gloss'].append(this_segment[1:-1])

            elif (scripts.script_type(this_segment) != scripts.Script.Ascii 
                    or this_segment.startswith('-')):
                # It must be a reading.
                char = this_segment[0]
                if char == '-':
                    char = this_segment[1]

                if scripts.script_type(char) == scripts.Script.Katakana:
                    kanji_info['on_readings'].append(this_segment)
                elif scripts.script_type(char) == scripts.Script.Hiragana:
                    kanji_info['kun_readings'].append(this_segment)
                else:
                    raise Exception, "Unknown segment %s" % this_segment

            elif this_segment in ('T1', 'T2'):
                continue

            else:
                # handle various codes
                code = this_segment[0]
                remainder = this_segment[1:]
                try:
                    remainder = int(remainder)
                except:
                    pass

                kanji_info.setdefault(remappings[code], []).append(
                    remainder)

        kanji_info['stroke_count'] = kanji_info['stroke_count'][0]
        if kanji_info.has_key('frequency'):
            kanji_info['frequency'] = int(kanji_info['frequency'][0])

        kanji_info['skip_code'] = tuple(map(
                int,
                kanji_info['skip_code'][0].split('-')
            ))

        kanjidic_entry = KanjidicEntry(kanji_info)

        return kanjidic_entry

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# PRIVATE
#----------------------------------------------------------------------------#

# An in-memory cached version.
_cached_kanjidic = None

#----------------------------------------------------------------------------#
