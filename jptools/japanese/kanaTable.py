# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# kanaTable.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 16:05:55 2007
#
#----------------------------------------------------------------------------#

u""" 
This module provides an interface to the consonant/vowel structure of the
Japanese hiragana and katakana syllabaries.
"""

#----------------------------------------------------------------------------#

import copy

#----------------------------------------------------------------------------#
# CONSTANTS
#----------------------------------------------------------------------------#

smallKana = u'ぁぃぅぇぉっょゅゃ'
nKana = u'ん'

#----------------------------------------------------------------------------#

class KanaTable(object):
    u"""
    An interface to the regular structure of the hiragana syllabary.

        >>> t = KanaTable()
        >>> k = t.toVowelLine(u'す')
        >>> k == u'う'
        True
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self):
        u"""
        Constructor. Initializes internal dictionaries to make later lookup
        faster. 
        """
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

        toConsonantLine = {}
        for cLine, elems in self._table.iteritems():
            toConsonantLine.update([(e, cLine) for e in elems])
        self._toConsonantLine = toConsonantLine

        toVowelLine = {}
        for vowelLine in apply(zip, self._table.values()):
            vowelLine = list(sorted(vowelLine))
            vowel = vowelLine[0]
            toVowelLine.update([(k, vowel) for k in vowelLine])
        self._toVowelLine = toVowelLine
        return

    #------------------------------------------------------------------------#

    def getCoords(self, kana):
        u"""
        Returns the pair (consonant line, vowel line) for the given kana
        character.
        """
        if not self._toConsonantLine or not self._toVowelLine:
            self._buildDicts()

        return (self._toConsonantLine(kana), self._toVowelLine(kana))

    #------------------------------------------------------------------------#

    def toVowelLine(self, kana):
        u"""Returns the vowel line of the given kana."""
        return self._toVowelLine[kana]

    #------------------------------------------------------------------------#

    def toConsonantLine(self, kana):
        u"""Returns the consonant line of the given kana."""
        return self._toConsonantLine[kana]

    #------------------------------------------------------------------------#

    def getTable(self):
        u"""Return the kana table itself."""
        return copy.deepcopy(self._table)

    #------------------------------------------------------------------------#

    @classmethod
    def getCached(cls):
        u"""Fetch a memory-cached copy of this class."""
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

