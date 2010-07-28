# -*- coding: utf-8 -*-
# 
#  split_by_codes.py
#  cjktools
#  
#  Created by Lars Yencken on 2007-06-13.
#  Copyright 2007-2010 Lars Yencken. All rights reserved.
# 

import re

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

        codes = set()
        for sense in entry.senses:
            codes.update(get_codes(sense))

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
        codes = set()
        for sense in entry.senses:
            codes.update(get_codes(sense))
        yield entry, codes

#----------------------------------------------------------------------------#

_code_pattern = re.compile(
        u'^\(([a-zA-Z][A-Z0-9]*(,[a-zA-Z][A-Z0-9]*)*)\)',
        re.UNICODE,
    )

# taken from http://www.csse.monash.edu.au/~jwb/edict_doc.html (2010-07-28)
_known_codes = set(['Buddh', 'MA', 'X', 'abbr', 'adj', 'adj-f', 'adj-i',
    'adj-na', 'adj-no', 'adj-pn', 'adj-t', 'adv', 'adv-n', 'adv-to', 'arch',
    'ateji', 'aux', 'aux-adj', 'aux-v', 'chn', 'col', 'comp', 'conj', 'ctr',
    'derog', 'eK', 'ek', 'exp', 'fam', 'fem', 'food', 'geom', 'gikun', 'gram',
    'hon', 'hum', 'iK', 'id', 'int', 'io', 'iv', 'ling', 'm-sl', 'male',
    'male-sl', 'math', 'mil', 'n', 'n-adv', 'n-pref', 'n-suf', 'n-t', 'ng',
    'num', 'oK', 'obs', 'obsc', 'ok', 'on-mim', 'physics', 'pn', 'poet',
    'pol', 'pref', 'prt', 'rare', 'sens', 'sl', 'suf', 'uK', 'uk', 'v1', 'v5',
    'v5aru', 'v5b', 'v5g', 'v5k', 'v5k-s', 'v5m', 'v5n', 'v5r', 'v5r-i',
    'v5s', 'v5t', 'v5u', 'v5u-s', 'v5uru', 'v5z', 'vi', 'vk', 'vn', 'vs',
    'vs-i', 'vs-s', 'vt', 'vulg', 'vz', 's', 'p', 'u', 'g', 'f', 'm', 'h',
    'pr', 'co', 'st'])

def get_codes(sense):
    "Returns the dictionary codes found in the given line."
    match = _code_pattern.match(sense)
    if match:
        return [c for c in match.group(1).split(',') for c in _known_codes]
    else:
        return []
  
# vim: ts=4 sw=4 sts=4 et tw=78: