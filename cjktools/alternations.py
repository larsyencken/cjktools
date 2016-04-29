# -*- coding: utf-8 -*-
#
#  alternations.py
#  cjktools
#

"""
This module deals with sound and reading alternations, both predicting and
recovering from them.
"""

from __future__ import unicode_literals

from cjktools import kana_table
from cjktools import scripts
from cjktools import maps

from six import unichr as chr
from six import iteritems

import re
from itertools import product

_sokuon_map = {scripts.Script.Hiragana: 'っ',
               scripts.Script.Katakana: 'ッ'}

_onbin_map = {scripts.Script.Hiragana: 'いちりきつく',
              scripts.Script.Katakana: 'イチリキツク'}


def canonical_forms(kana_segments):
    """
    When given a sequence of segments, determine all possible canonical
    forms for the sequence. We define the canonical form to be the
    underlying form, before sequential voicing and sound euphony are
    applied.

    :param kana_segments:
        Reading segments in their surface form.
    """
    num_segments = len(kana_segments)

    candidate_sets = []
    for i, segment in enumerate(kana_segments):
        left_context = i > 0
        right_context = i < num_segments - 1
        variants = canonical_segment_forms(segment,
                                           left_context=left_context,
                                           right_context=right_context)

        candidate_sets.append(variants)

    return list(product(*candidate_sets))


def canonical_segment_forms(segment, left_context=True, right_context=True):
    """
    When given a single segment, determine all possible canonical forms
    for that segment, assuming that both sequential voicing and
    sound euphony were possible (i.e. that the segment had both left
    and right context).
    """
    table = kana_table.KanaTable.get_cached()
    variants = set([segment])
    stype = scripts.script_type(segment)
    sokuon = _sokuon_map.get(stype, None)
    onbin = _onbin_map.get(stype, None)

    if sokuon is None:
        raise ValueError('Unsupported script type. '
                         'Segments must be hiragana or katakana')

    if right_context and len(segment) > 1 and segment.endswith(sokuon):
        # Can restore onbin cases
        variants.update([segment[:-1] + c for c in onbin])

    if left_context and table.is_voiced(segment[0]):
        # Can devoice
        variants.update([from_voiced[v[0]] + v[1:] for v in variants])

    return variants


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

    return list(product(*candidate_sets))


def rendaku_variants(kana_segment):
    """
    Determine the possible variants of a single kana segment.
    """
    variants = set([kana_segment])
    for kana in to_voiced[kana_segment[0]]:
        variants.add(kana + kana_segment[1:])
    return variants


def onbin_variants(kana_segment):
    """
    Determine the sound euphony variants of a kana segment.
    """
    variants = set([kana_segment])
    if len(kana_segment) > 1:
        sokuon = _sokuon_map[scripts.script_type(kana_segment)]
        variants.add(kana_segment[:-1] + sokuon)

    return variants


def _create_voicing_map():
    """
    Constructs map from kana to their voiced alternatives.
    """
    table = kana_table.KanaTable.get_cached().get_table()
    voiced_line = table['か'] + table['さ'] + table['た']
    double_voiced_line = table['は']

    voicing_map = {}
    for kana in scripts.get_script(scripts.Script.Hiragana):
        ord_kana = ord(kana)

        if kana in voiced_line:
            voicing_map[kana] = [chr(ord_kana+1)]
        elif kana in double_voiced_line:
            voicing_map[kana] = [chr(ord_kana+1), chr(ord_kana+2)]
        else:
            voicing_map[kana] = []

    # Add katakana into the mix
    katakana_vm = {scripts.to_katakana(k): list(map(scripts.to_katakana, v))
                   for k, v in iteritems(voicing_map)}

    voicing_map.update(katakana_vm)

    return voicing_map

to_voiced = _create_voicing_map()
from_voiced = maps.invert_mapping(to_voiced)
from_voiced = dict((k, v[0]) for (k, v) in iteritems(from_voiced))


def insert_duplicate_kanji(kanji_string):
    """
    Inserts full kanji for characters where a shorthand is used.

        >>> k = insert_duplicate_kanji(u'私々')
        >>> expected = u'私私'
        >>> k == expected
        True
    """
    loc = kanji_string.find('々')
    while loc > 0:
        dup = kanji_string[loc-1]
        kanji_string = kanji_string[:loc] + dup + kanji_string[loc+1:]
        loc = kanji_string.find('々')

    return kanji_string


_long_finder = re.compile(r'(?<=[\u3041-\u3096])ー')  # Finds only in hiragana


def expand_long_vowels(kana_string):
    """
    Expands whatever long vowels are possible to expand.

        >>> a = expand_long_vowels(u'すー')
        >>> b = u'すう'
        >>> a == b
        True
    """
    script_converters = {scripts.Script.Hiragana: lambda x: x,
                         scripts.Script.Katakana: scripts.to_katakana}

    table = kana_table.KanaTable.get_cached()

    out_string = ''
    for segment in scripts.script_boundaries(kana_string):
        if len(segment):
            char_type = scripts.script_type(segment)

            if char_type not in script_converters:
                out_string += segment
                continue

            reverse_operation = script_converters[char_type]
            segment = scripts.to_hiragana(segment)
        else:
            continue

        for m in _long_finder.finditer(segment):
            i = m.start()
            vowel = table.to_vowel_line(segment[i-1])
            segment = segment[:i] + vowel + segment[i+1:]

        out_string += reverse_operation(segment)

    return out_string
