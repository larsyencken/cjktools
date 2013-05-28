# -*- coding: utf-8 -*-
#
#  kanjidic.py
#  cjktools
#

"""
A nice interface to the Kanjidic dictionary.
"""

import re
from itertools import chain

from cjktools import scripts
from cjktools.common import sopen

import cjkdata


basic_features = set([
    'gloss',
    'stroke_count',
    'jyouyou_grade',
    'skip_code',
    'onyomi',
    'kunyomi',
    'unicode'
])

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


class KanjidicEntry(object):
    "A single entry in the kanjidic file."

    def __init__(self, **entry_details):
        assert ('on_readings' in entry_details
                and 'kun_readings' in entry_details)
        self.__dict__.update(entry_details)

    def get_all_readings(self):
        "Construct a reading pool for this entry."
        reading_set = set()
        for reading in (self.kun_readings +
                        map(scripts.to_hiragana, self.on_readings)):
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


class Kanjidic(dict):
    """
    An interface to the kanjidic dictionary. Create a new instance to parse
    the dictionary. Has a nice getitem interface to get the details of a
    character.
    """

    def __init__(self, kanjidic_files=None):
        dict.__init__(self)

        if kanjidic_files is None:
            kanjidic_files = [
                cjkdata.get_resource('kanjidic'),
                cjkdata.get_resource('kanjd212'),
            ]

        line_stream = reduce(chain, [sopen(f) for f in kanjidic_files])
        self._parse_kanjidic(line_stream)

    @classmethod
    def get_cached(cls):
        if not hasattr(cls, '_cached'):
            cls._cached = cls()

        return cls._cached

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
            self[entry.kanji] = entry

    def _parse_line(self, line):
        "Parses a single line in the kanjdic file, returning an entry."
        segment_pattern = re.compile('[^ {]+|{.*?}', re.UNICODE)
        segments = segment_pattern.findall(line.strip())
        segments.reverse()

        kanji = segments.pop()
        jis_code = int(segments.pop(), 16)
        info = {
            'kanji':        kanji,
            'gloss':        [],
            'on_readings':  [],
            'kun_readings': [],
            'jis_code':     jis_code
        }

        while segments:
            s = segments.pop()

            if s.startswith('{'):
                info['gloss'].append(s[1:-1])

            elif (scripts.script_type(s) != scripts.Script.Ascii
                    or s.startswith('-')):
                # It must be a reading.
                char = s[0]
                if char == '-':
                    char = s[1]

                if scripts.script_type(char) == scripts.Script.Katakana:
                    info['on_readings'].append(s)
                elif scripts.script_type(char) == scripts.Script.Hiragana:
                    info['kun_readings'].append(s)
                else:
                    raise Exception("Unknown segment %s" % s)

            elif s in ('T1', 'T2'):
                continue

            else:
                # handle various codes
                code = s[0]
                remainder = s[1:]
                try:
                    remainder = int(remainder)
                except:
                    pass

                info.setdefault(remappings.get(code, code), []).append(
                    remainder)

        info['stroke_count'] = info['stroke_count'][0]
        if 'frequency' in info:
            info['frequency'] = info['frequency'][0]

        info['skip_code'] = tuple(int(i)
                                  for i in info['skip_code'][0].split('-'))

        return KanjidicEntry(**info)


_cached_kanjidic = None
