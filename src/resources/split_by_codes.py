#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# split_by_codes.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Jun 13 10:10:23 EST 2007
#
#----------------------------------------------------------------------------#

import os, sys, optparse
import re
from cjktools.common import sopen

from auto_format import iter_entries

#----------------------------------------------------------------------------#
# PUBLIC
#----------------------------------------------------------------------------#

def load_coded_dictionary(filename):
    """
    Load a dictionary which is split by the codes within it.
    """
    word_to_entry = {} 
    coded_dict = {}
    for entry in iter_entries(filename):
        word = entry.word

        # Merge any word entries with the same graphical form.
        if word in word_to_entry:
            first_entry = word_to_entry[word]
            first_entry.update(entry)
            entry = first_entry
        else:
            word_to_entry[word] = entry

        codes = get_codes('/'.join(entry.senses))

        # Create a subset of the dictionary for each code.
        for code in codes:
            sub_dict = coded_dict.setdefault(code, {})

            # Note that overwriting is ok, since we already merged any
            # coincidental forms.
            sub_dict[word] = entry

    return coded_dict

#----------------------------------------------------------------------------#

def iter_coded_entries(filename):
    """
    Returns an iterator over dictionary entries in the filename, with their
    parsed codes, in (entry, code_list) pairs.
    """
    for entry in iter_entries(filename):
        codes = get_codes('/'.join(entry.senses))
        yield entry, codes

    return

#----------------------------------------------------------------------------#

_code_pattern = re.compile(u'\(([a-z,]+)\)', re.UNICODE)

def get_codes(line, filter_set=[]):
    """
    Returns the dictionary codes found in the given line. 
    """
    matches = _code_pattern.findall(line)
    codes = []
    for match in matches:
        if ' ' not in match:
            codes.extend([c for c in match.split(',') if c not in filter_set])

    return codes
 
#----------------------------------------------------------------------------#

_english_words = '/usr/share/dict/words'

def split_by_codes(input_file, output_file, ignores=[]):
    """
    Splits the dictionary into separate files based on the codes present.
    """
    i_stream = sopen(input_file, 'r')
    o_stream = sopen(output_file, 'w')

    known_words = set([l.rstrip().lower() for l in open(_english_words)])
    known_words = set([w for w in known_words if len(w) > 3])

    code_streams = {}

    lines = iter(i_stream)
    header = i_stream.next()

    for line in i_stream:
        codes = get_codes(line, known_words)

        for code in codes:
            o_stream = code_streams.get(code)
            if o_stream is None:
                print 'Found new code: %s' % code
                o_stream = code_streams.setdefault(
                        code, 
                        sopen('%s.%s' % (output_file, code), 'w')
                    )
                o_stream.write(header)
            o_stream.write(line)

    i_stream.close()

    for o_stream in code_streams.values():
        o_stream.close()

    return

#----------------------------------------------------------------------------#
# PRIVATE
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# MODULE EPILOGUE
#----------------------------------------------------------------------------#

def _create_option_parser():
    """
    Creates an option parser instance to handle command-line options.
    """
    usage = \
"""%prog [options] input_file output_file

Splits an edict format dictionary into multiple files by the codes used."""

    parser = optparse.OptionParser(usage)

    parser.add_option('--debug', action='store_true', dest='debug',
            default=False, help='Enables debugging mode [False]')

    parser.add_option('--ignore', '-i', action='store', dest='ignore',
            default='', help='A comma separated list of tags to ignore.')

    return parser

#----------------------------------------------------------------------------#

def main(argv):
    """
    The main method for this module.
    """
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    try:
        [input_file, output_file] = args
    except:
        parser.print_help()
        sys.exit(1)

    # Avoid psyco in debugging mode, since it merges stack frames.
    if not options.debug:
        try:
            import psyco
            psyco.profile()
        except:
            pass

    split_by_codes(input_file, output_file, ignores=options.ignore.split(','))
    
    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

#----------------------------------------------------------------------------#
  
# vim: ts=4 sw=4 sts=4 et tw=78:

