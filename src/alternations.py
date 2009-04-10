# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# alternations.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Jun 26 12:47:52 2007
#
#----------------------------------------------------------------------------#

"""
This module deals with sound and reading alternations, both predicting and
recovering from them. 
"""

#----------------------------------------------------------------------------#

import kana_table
import scripts
import maps
import stats

#----------------------------------------------------------------------------#

def canonical_forms(kana_segments):
    """
    When given a sequence of segments, determine all possible canonical
    forms for the sequence. We define the canonical form to be the
    underlying form, before sequential voicing and sound euphony are
    applied.

    @param kana_segments: Reading segments in their surface form.
    """
    table = kana_table.KanaTable.get_cached()
    num_segments = len(kana_segments)

    candidate_sets = []
    for i, segment in enumerate(kana_segments):
        variants = [segment]

        if i < num_segments - 1 and len(segment) > 1 and \
                    segment.endswith(u'っ'):
            # Can restore onbin cases.
            variants.extend([segment[:-1] + c for c in u'いちりきつく'])

        if i > 0 and table.is_voiced(segment[0]):
            # Can devoice.
            variants.extend([from_voiced[v[0]] + v[1:] for v in variants])

        candidate_sets.append(variants)

    return stats.combinations(candidate_sets)

#----------------------------------------------------------------------------#

def canonical_segment_forms(segment, left_context=True, right_context=True):
    """
    When given a single segment, determine all possible canonical forms
    for that segment, assuming that both sequential voicing and
    sound euphony were possible (i.e. that the segment had both left
    and right context).
    """
    table = kana_table.KanaTable.get_cached()
    variants = set([segment])

    if right_context and len(segment) > 1 and segment.endswith(u'っ'):
        variants.update([segment[:-1] + c for c in u'いちりきつく'])

    if left_context and table.is_voiced(segment[0]):
        variants.update([from_voiced[v[0]] + v[1:] for v in variants])

    return variants

#----------------------------------------------------------------------------#

def surface_forms(reading_segments):
    """
    The counterpart of canonical_forms(). Takes a correct reading, and
    determines how it could be erroneously modified into various surface
    forms.
    """
    candidate_sets = []
    candidate_sets.append(onbin_variants(reading_segments[0]))
    candidate_sets.extend(
            map(rendaku_variants, reading_segments[1:])
        )

    return stats.combinations(candidate_sets)

#----------------------------------------------------------------------------#

def rendaku_variants(kana_segment):
    """
    Determine the possible variants of a single kana segment.
    """
    variants = set([kana_segment])
    for kana in to_voiced[kana_segment[0]]:
        variants.add(kana + kana_segment[1:])
    return variants

#----------------------------------------------------------------------------#

def onbin_variants(kana_segment):
    """
    Determine the sound euphony variants of a kana segment.
    """
    variants = set([kana_segment])
    if len(kana_segment) > 1:
        variants.add(kana_segment[:-1] + u'っ')

    return variants

#----------------------------------------------------------------------------#

def _create_voicing_map():
    """
    Constructs map from kana to their voiced alternatives.
    """
    table = kana_table.KanaTable.get_cached().get_table()
    voiced_line = table[u'か'] + table[u'さ'] + table[u'た']
    double_voiced_line = table[u'は']

    voicing_map = {}
    for kana in scripts.get_script(scripts.Script.Hiragana):
        ord_kana = ord(kana)

        if kana in voiced_line:
            voicing_map[kana] = [unichr(ord_kana+1)]
        elif kana in double_voiced_line:
            voicing_map[kana] = [unichr(ord_kana+1), unichr(ord_kana+2)]
        else:
            voicing_map[kana] = []

    return voicing_map

to_voiced = _create_voicing_map()
from_voiced = maps.invert_mapping(to_voiced)
from_voiced = dict((k, v[0]) for (k, v) in from_voiced.iteritems())

#----------------------------------------------------------------------------#

def insert_duplicate_kanji(kanji_string):
    """
    Inserts full kanji for characters where a shorthand is used.

        >>> k = insert_duplicate_kanji(unicode('私々', 'utf8'))
        >>> expected = unicode('私私', 'utf8')
        >>> k == expected
        True
    """
    loc = kanji_string.find(u'々')
    while loc > 0:
        dup = kanji_string[loc-1]
        kanji_string = kanji_string[:loc] + dup + kanji_string[loc+1:]
        loc = kanji_string.find(u'々')

    return kanji_string

#----------------------------------------------------------------------------#

def expand_long_vowels(kana_string):
    """
    Expands whatever long vowels are possible to expand.

        >>> a = expand_long_vowels(unicode('すー', 'utf8'))
        >>> b = unicode('すう', 'utf8')
        >>> a == b
        True
    """
    not_found = -1
    kana_string = scripts.to_hiragana(kana_string)
    table = kana_table.KanaTable.get_cached()

    i = kana_string.find(u'ー', 1)
    while i != not_found:
        previous_char = kana_string[i-1]
        previous_script = scripts.script_type(previous_char)
        if previous_script == scripts.Script.Hiragana:
            # Ok, we can correct this one.
            vowel = table.to_vowel_line(previous_char)
            kana_string = kana_string[:i] + vowel + kana_string[i+1:]

        i = kana_string.find(u'ー', i+1)

    return kana_string

#----------------------------------------------------------------------------#
