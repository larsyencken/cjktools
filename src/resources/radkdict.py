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
        @param dict_file: The radkfile to parse.
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
        radical_to_kanji = {}
        radical_to_stroke_count = {}

        current_radical = None
        stroke_count = None

        for line in line_stream:
            if line.startswith('#'):
                # found a comment line
                continue

            if line.startswith('$'):
                # found a line with a new radical
                dollar, current_radical, stroke_count = line.split()
                radical_to_stroke_count[current_radical] = int(stroke_count)
                continue

            # found a line of kanji
            kanji = line.strip()
            radical_to_kanji.setdefault(current_radical, []).extend(kanji)

        self.update(maps.invert_mapping(radical_to_kanji))
        maps.map_dict(tuple, self, in_place=True)

        self.radical_to_stroke_count = radical_to_stroke_count
        self.radical_to_kanji = radical_to_kanji

        return

    #------------------------------------------------------------------------#

    @classmethod
    def get_cached(cls):
        "Returns a memory-cached class instance."
        if not hasattr(cls, '_cached'):
            cls._cached = cls()

        return cls._cached

#----------------------------------------------------------------------------#

def print_radicals(kanji_list):
    "Print out each kanji and the radicals it contains."
    radical_dict = RadkDict()
    for kanji in kanji_list:
        kanji = unicode(kanji, 'utf8')
        radicals = radical_dict[kanji]

        print '%s: ' % kanji, ' '.join(sorted(radicals))

    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    print_radicals(sys.argv[1:])

