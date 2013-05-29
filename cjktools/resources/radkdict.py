#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  radkdict.py
#  cjktools
#

"Based on the radkfile, a dictionary mapping character to bag of radicals."

import sys

import codecs
from cjktools import maps

import cjkdata


class RadkDict(dict):
    "Determines which radicals a character contains."

    def __init__(self, istream=None):
        """
        @param dict_file: The radkfile to parse.
        """
        if istream is None:
            istream = open(cjkdata.get_resource('radkfile'))

        self._parse_radkfile(codecs.getreader('utf8')(istream))

    def _parse_radkfile(self, line_stream):
        """
        Parses the radkfile and populates the current dictionary.

        @param filename: The radkfile to parse.
        """
        radical_to_kanji = {}
        radical_to_stroke_count = {}

        current_radical = None
        stroke_count = None

        for line in line_stream:
            line = line.rstrip()
            if line.startswith('#'):
                # found a comment line
                continue

            if line.startswith('$'):
                # found a line with a new radical
                parts = line.split()
                if len(parts) not in (3, 4):
                    raise Exception('format error parsing radkfile')

                dollar, current_radical, stroke_count = parts[:3]
                radical_to_stroke_count[current_radical] = int(stroke_count)
                continue

            # found a line of kanji
            kanji = line.strip()
            radical_to_kanji.setdefault(current_radical, []).extend(kanji)

        self.update(maps.invert_mapping(radical_to_kanji))
        maps.map_dict(tuple, self, in_place=True)

        self.radical_to_stroke_count = radical_to_stroke_count
        self.radical_to_kanji = radical_to_kanji

    @classmethod
    def get_cached(cls):
        "Returns a memory-cached class instance."
        if not hasattr(cls, '_cached'):
            cls._cached = cls()

        return cls._cached


def print_radicals(kanji_list):
    "Print out each kanji and the radicals it contains."
    radical_dict = RadkDict()
    for kanji in kanji_list:
        kanji = unicode(kanji, 'utf8')
        radicals = radical_dict[kanji]

        print '%s: ' % kanji, ' '.join(sorted(radicals))


if __name__ == '__main__':
    print_radicals(sys.argv[1:])
