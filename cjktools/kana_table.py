# -*- coding: utf-8 -*-
#
#  kana_table.py
#  cjktools
#

"""
This module provides an interface to the consonant/vowel structure of the
Japanese hiragana and katakana syllabaries.
"""
from __future__ import unicode_literals

import copy
from six import iteritems, text_type

small_kana = 'ぁぃぅぇぉっょゅゃ'
n_kana = 'ん'


class KanaTable(object):
    """
    An interface to the regular structure of the hiragana syllabary.

        >>> t = KanaTable()
        >>> t.to_vowel_line(unicode('す', 'utf8')) == unicode('う', 'utf8')
        True
    """

    def __init__(self):
        """
        Constructor. Initializes internal dictionaries to make later lookup
        faster.
        """
        self.vowels = 'あいうえお'
        self.consonants = 'かがさざただまはばぱなら'
        self.voiced_consonants = set('がだざびぴじばぱ')
        self._table = {
            'あ': 'あいうえお',
            'か': 'かきくけこ',
            'が': 'がぎぐげご',
            'さ': 'さしすせそ',
            'ざ': 'ざじずぜぞ',
            'た': 'たちつてと',
            'だ': 'だぢづでど',
            'ま': 'まみむめも',
            'は': 'はひふへほ',
            'ば': 'ばびぶべぼ',
            'ぱ': 'ぱぴぷぺぽ',
            'な': 'なにぬねの',
            'ら': 'らりるれろ'
        }

        to_consonant_line = {}
        for c_line, elems in iteritems(self._table):
            to_consonant_line.update([(e, c_line) for e in elems])
        self._to_consonant_line = to_consonant_line

        to_vowel_line = {}
        for vowel_line in zip(*self._table.values()):
            vowel_line = list(sorted(vowel_line))
            vowel = vowel_line[0]
            to_vowel_line.update([(k, vowel) for k in vowel_line])
        self._to_vowel_line = to_vowel_line
        return

    def get_coords(self, kana):
        """
        Returns the pair (consonant line, vowel line) for the given kana
        character.
        """
        if not self._to_consonant_line or not self._to_vowel_line:
            self._build_dicts()

        return (self._to_consonant_line[kana], self._to_vowel_line[kana])

    def from_coords(self, consonant, vowel):
        """
        Converts a consonant and vowel pair to a single kana, provided they
        generate a member of the table.
        """
        return self._table[consonant][self.vowels.index(vowel)]

    def to_vowel_line(self, kana):
        """Returns the vowel line of the given kana."""
        if kana == 'わ':
            return 'あ'
        else:
            return self._to_vowel_line.get(kana)

    def to_consonant_line(self, kana):
        """Returns the consonant line of the given kana."""
        return self._to_consonant_line.get(kana)

    def is_voiced(self, kana):
        """Returns True if the kana is voiced, False otherwise."""
        return self.to_consonant_line(kana) in self.voiced_consonants

    def get_table(self):
        """Return the kana table itself."""
        return copy.deepcopy(self._table)

    @classmethod
    def get_cached(cls):
        """Fetch a memory-cached copy of this class."""
        if not hasattr(cls, '_cached'):
            cls._cached = KanaTable()

        return cls._cached

    def __unicode__(self):
        return '<KanaTable object %s>' % hash(self)

    def __repr__(self):
        return text_type(self).encode('utf8')
