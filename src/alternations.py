# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# alternations.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Jun 26 12:47:52 2007
#
#----------------------------------------------------------------------------#

"""
This module deals with sound and reading alternations, both predicting and
recovering from them. 
"""

#----------------------------------------------------------------------------#

import kanaTable
import maps
import stats

#----------------------------------------------------------------------------#

def canonicalForms(kanaSegments):
    """
    When given a sequence of segments, determine all possible canonical
    forms for the sequence. We define the canonical form to be the
    underlying form, before sequential voicing and sound euphony are
    applied.

    @param kanaSegments: Reading segments in their surface form.
    """

    numSegments = len(kanaSegments)

    candidateSets = []
    for i, segment in enumerate(kanaSegments):
        variants = [segment]

        if i < numSegments - 1 and len(segment) > 1 and \
                    segment.endswith(u'っ'):
            # Can restore onbin cases.
            variants.extend([segment[:-1] + c for c in u'いちりきつく'])

        if i > 0 and isVoiced(segment[0]):
            # Can devoice.
            variants.extend([fromVoiced[v[0]] + v[1:] for v in variants])

        candidateSets.append(variants)

    return stats.combinations(candidateSets)

#----------------------------------------------------------------------------#

def canonicalSegmentForms(segment, leftContext=True, rightContext=True):
    """
    When given a single segment, determine all possible canonical forms
    for that segment, assuming that both sequential voicing and
    sound euphony were possible (i.e. that the segment had both left
    and right context).
    """
    variants = set([segment])

    if rightContext and len(segment) > 1 and segment.endswith(u'っ'):
        variants.update([segment[:-1] + c for c in u'いちりきつく'])

    if leftContext and isVoiced(segment[0]):
        variants.update([fromVoiced[v[0]] + v[1:] for v in variants])

    return variants

#----------------------------------------------------------------------------#

def surfaceForms(readingSegments):
    """
    The counterpart of canonicalForms(). Takes a correct reading, and
    determines how it could be erroneously modified into various surface
    forms.
    """
    candidateSets = []
    candidateSets.append(onbinVariants(readingSegments[0]))
    candidateSets.extend(
            map(rendakuVariants, readingSegments[1:])
        )

    return stats.combinations(candidateSets)

#----------------------------------------------------------------------------#

def rendakuVariants(kanaSegment):
    """
    Determine the possible variants of a single kana segment.
    """
    variants = set([kanaSegment])
    for kana in toVoiced[kanaSegment[0]]:
        variants.add(kana + kanaSegment[1:])
    return variants

#----------------------------------------------------------------------------#

def onbinVariants(kanaSegment):
    """
    Determine the sound euphony variants of a kana segment.
    """
    variants = set([kanaSegment])
    if len(kanaSegment) > 1:
        variants.add(kanaSegment[:-1] + u'っ')

    return variants

#----------------------------------------------------------------------------#

def _createVoicingMap():
    """
    Constructs map from kana to their voiced alternatives.
    """
    table = kanaTable.KanaTable.getCached().getTable()
    voicedLine = table[u'か'] + table[u'さ'] + table[u'た']
    doubleVoicedLine = table[u'は']

    voicingMap = {}
    for kana in getScript(Script.Hiragana):
        ordKana = ord(kana)

        if kana in voicedLine:
            voicingMap[kana] = [unichr(ordKana+1)]
        elif kana in doubleVoicedLine:
            voicingMap[kana] = [unichr(ordKana+1), unichr(ordKana+2)]
        else:
            voicingMap[kana] = []

    return voicingMap

toVoiced = _createVoicingMap()
fromVoiced = maps.invertMapping(toVoiced)
fromVoiced = dict((k, v[0]) for (k, v) in fromVoiced.iteritems())

#----------------------------------------------------------------------------#

def insertDuplicateKanji(kanjiString):
    """
    Inserts full kanji for characters where a shorthand is used.
    """
    loc = kanjiString.find(u'々')
    while loc > 0:
        dup = kanjiString[loc-1]
        kanjiString = kanjiString[:loc] + dup + kanjiString[loc+1:]
        loc = kanjiString.find(u'々')

    return kanjiString

#----------------------------------------------------------------------------#

def isVoiced(char):
    """
    Returns True if the character is a kana character which is voiced.
    """
    char = toHiragana(char)

    line = kanaLine.get(char)
    if not line:
        # Not a kana character.
        return False

    return line in u'がだざばぱ'

#----------------------------------------------------------------------------#

def expandLongVowels(kanaString):
    """
    Expands whatever long vowels are possible to expand.
    """
    notFound = -1
    kanaString = toHiragana(kanaString)

    i = kanaString.find(u'ー', 1)
    while i != notFound:
        previousChar = kanaString[i-1]
        previousScript = scriptType(previousChar)
        if previousScript == Script.Hiragana:
            # Ok, we can correct this one.
            vowel = vowelLine(previousChar)
            kanaString = kanaString[:i] + vowel + kanaString[i+1:]

        i = kanaString.find(u'ー', i+1)

    return kanaString

#----------------------------------------------------------------------------#
