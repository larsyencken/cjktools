# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# kanaTable.py
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

smallKana = u'ぁぃぅぇぉっょゅゃ'
nKana = u'ん'

#----------------------------------------------------------------------------#

class KanaTable(object):
    """
    An interface to the regular structure of the hiragana syllabary.

        >>> t = KanaTable()
        >>> t.toVowelLine(unicode('す', 'utf8')) == unicode('う', 'utf8')
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
        self.voicedConsonants = set(u'がだざびぴじばぱ')
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
        """
        Returns the pair (consonant line, vowel line) for the given kana
        character.
        """
        if not self._toConsonantLine or not self._toVowelLine:
            self._buildDicts()

        return (self._toConsonantLine[kana], self._toVowelLine[kana])

    #------------------------------------------------------------------------#

    def fromCoords(self, consonant, vowel):
        """
        Converts a consonant and vowel pair to a single kana, provided they
        generate a member of the table. 
        """
        return self._table[consonant][self.vowels.index(vowel)]

    #------------------------------------------------------------------------#

    def toVowelLine(self, kana):
        """Returns the vowel line of the given kana."""
        if kana == u'わ':
            return u'あ'
        else:
            return self._toVowelLine.get(kana)

    #------------------------------------------------------------------------#

    def toConsonantLine(self, kana):
        """Returns the consonant line of the given kana."""
        return self._toConsonantLine.get(kana)

    #------------------------------------------------------------------------#

    def isVoiced(self, kana):
        """Returns True if the kana is voiced, False otherwise."""
        return self.toConsonantLine(kana) in self.voicedConsonants

    #------------------------------------------------------------------------#

    def getTable(self):
        """Return the kana table itself."""
        return copy.deepcopy(self._table)

    #------------------------------------------------------------------------#

    @classmethod
    def getCached(cls):
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
