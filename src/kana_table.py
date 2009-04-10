# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# kana_table.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 16:05:55 2007
#
#----------------------------------------------------------------------------#

""" 
This module provides an interface to the consonant/vowel structure of the
Japanese hiragana and katakana syllabaries.
"""

#----------------------------------------------------------------------------#

import copy

#----------------------------------------------------------------------------#
# CONSTANTS
#----------------------------------------------------------------------------#

small_kana = u'ぁぃぅぇぉっょゅゃ'
n_kana = u'ん'

#----------------------------------------------------------------------------#

class KanaTable(object):
    """
    An interface to the regular structure of the hiragana syllabary.

        >>> t = KanaTable()
        >>> t.to_vowel_line(unicode('す', 'utf8')) == unicode('う', 'utf8')
        True
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self):
        """
        Constructor. Initializes internal dictionaries to make later lookup
        faster. 
        """
        self.vowels = u'あいうえお'
        self.consonants = u'かがさざただまはばぱなら'
        self.voiced_consonants = set(u'がだざびぴじばぱ')
        self._table = {
            u'あ': u'あいうえお',
            u'か': u'かきくけこ',
            u'が': u'がぎぐげご',
            u'さ': u'さしすせそ',
            u'ざ': u'ざじずぜぞ',
            u'た': u'たちつてと',
            u'だ': u'だぢづでど',
            u'ま': u'まみむめも',
            u'は': u'はひふへほ',
            u'ば': u'ばびぶべぼ',
            u'ぱ': u'ぱぴぷぺぽ',
            u'な': u'なにぬねの',
            u'ら': u'らりるれろ'
        }

        to_consonant_line = {}
        for c_line, elems in self._table.iteritems():
            to_consonant_line.update([(e, c_line) for e in elems])
        self._to_consonant_line = to_consonant_line

        to_vowel_line = {}
        for vowel_line in apply(zip, self._table.values()):
            vowel_line = list(sorted(vowel_line))
            vowel = vowel_line[0]
            to_vowel_line.update([(k, vowel) for k in vowel_line])
        self._to_vowel_line = to_vowel_line
        return

    #------------------------------------------------------------------------#

    def get_coords(self, kana):
        """
        Returns the pair (consonant line, vowel line) for the given kana
        character.
        """
        if not self._to_consonant_line or not self._to_vowel_line:
            self._build_dicts()

        return (self._to_consonant_line[kana], self._to_vowel_line[kana])

    #------------------------------------------------------------------------#

    def from_coords(self, consonant, vowel):
        """
        Converts a consonant and vowel pair to a single kana, provided they
        generate a member of the table. 
        """
        return self._table[consonant][self.vowels.index(vowel)]

    #------------------------------------------------------------------------#

    def to_vowel_line(self, kana):
        """Returns the vowel line of the given kana."""
        if kana == u'わ':
            return u'あ'
        else:
            return self._to_vowel_line.get(kana)

    #------------------------------------------------------------------------#

    def to_consonant_line(self, kana):
        """Returns the consonant line of the given kana."""
        return self._to_consonant_line.get(kana)

    #------------------------------------------------------------------------#

    def is_voiced(self, kana):
        """Returns True if the kana is voiced, False otherwise."""
        return self.to_consonant_line(kana) in self.voiced_consonants

    #------------------------------------------------------------------------#

    def get_table(self):
        """Return the kana table itself."""
        return copy.deepcopy(self._table)

    #------------------------------------------------------------------------#

    @classmethod
    def get_cached(cls):
        """Fetch a memory-cached copy of this class."""
        if not hasattr(cls, u'_cached'):
            cls._cached = KanaTable()

        return cls._cached

    #------------------------------------------------------------------------#

    def __unicode__(self):
        return u'<KanaTable object %s>' % hash(self)

    def __repr__(self):
        return unicode(self).encode(u'utf8')

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
