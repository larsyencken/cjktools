# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# __init__.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Sun May 15 23:12:04 EST 2005
#
#----------------------------------------------------------------------------#

u"""
This module is responsible for Japanese script/encoding specific methods,
especially determining the script type of an entry. It is thus the only
module which requires a utf8 encoding for the additional Japanese characters.
"""

#----------------------------------------------------------------------------#

from .. import enum

#----------------------------------------------------------------------------#
# CONSTANTS
#----------------------------------------------------------------------------#

Script = enum.Enum(u'Hiragana', u'Katakana', u'Kanji', u'Ascii',
        u'FullAscii', u'Unknown')

_knownBands = {
        Script.Ascii:       (u'\u0021', u'\u00ff'),
        Script.Hiragana:	(u'\u3041', u'\u3096'),
        Script.Katakana:	(u'\u30a1', u'\u30f6'),
        Script.Kanji:	    (u'\u4e00', u'\u9fa5'),
        Script.FullAscii:	(u'\uff01', u'\uff5f'),
    }

_interKanaDistance = 96

#----------------------------------------------------------------------------#

class ScriptMapping:
    u"""
    A mapping function between two scripts. We assume that the given scripts
    are different versions of the same characters, and further that they are
    aligned at the start and end points stored.
    """
    def __init__(self, fromScript, toScript):
        u"""
        Constructor, initializes script conversion.
        
        @param fromScript: The script to convert from.
        @type fromScript: Script
        @param toScript: The script to convert to.
        @type toScript: Script
        """
        self.fromStart, self.fromEnd = _knownBands[fromScript]
        self.toStart, self.toEnd = _knownBands[toScript]
        self.ordDiff = ord(self.toStart) - ord(self.fromStart)
        assert (ord(self.fromEnd) - ord(self.fromStart)) <= \
                (ord(self.toEnd) - ord(self.toStart))
        return

    def __call__(self, jString):
        u"""
        Converts any matching characters in the given string between scripts.
        Any characters which don't match the input script are passed through
        unchanged.
        """
        result = []
        for char in jString:
            if self.fromStart <= char <= self.fromEnd:
                result.append(unichr(ord(char) + self.ordDiff))
            else:
                result.append(char)

        return u''.join(result)

toHiragana = ScriptMapping(Script.Katakana, Script.Hiragana)
toKatakana = ScriptMapping(Script.Hiragana, Script.Katakana)

#----------------------------------------------------------------------------#

_mappedChars = {
            u'\u3000':  u'\u0020',
            u'\u3001':  u'\u002c',
            u'\u3002':  u'\u002e',
        }

_toAscii = ScriptMapping(Script.FullAscii, Script.Ascii)

def normalizeAscii(jString):
    u"""
    Normalize a double-width ascii string, converting all characters to
    their single-width counterparts.

    @param jString: The string to convert.
    @type jString: unicode
    @return: The converted string.
    """
    result = []
    for char in jString:
        result.append(_mappedChars.get(char, char))

    return _toAscii(u''.join(result))

#----------------------------------------------------------------------------#

def getScript(script):
    u"""Returns a string containing all charcters in the given script."""

    scriptStarts, scriptEnds = _knownBands[script]

    output = []
    for i in xrange(ord(scriptStarts), ord(scriptEnds) + 1):
        output.append(unichr(i))

    return ''.join(output)

#----------------------------------------------------------------------------#

def compareKana(jStringA, jStringB):
    u"""
    Compares two kana strings in a script-independent manner.

    @type jStringA: unicode
    @type jStringB: unicode
    """
    return cmp(toKatakana(jStringA), toKatakana(jStringB))

#----------------------------------------------------------------------------#

def containsScript(script, jString):
    u"""
    Returns True if the given script is within the string, False
    otherwise.
    
    @param script: The script to search for.
    @type script: Script
    @param jString: The string to search within.
    @type jString: unicode
    """
    return script in scriptTypes(jString)

#----------------------------------------------------------------------------#

def scriptType(char):
    u"""
    Determine the type of script contained in the given character. Script
    types are expressed using the Script enum.

    @param char: The character to examine.
    @type char: unicode
    @return: The script type.   
    """
    # Normalize/typecheck our input.
    char = unicode(char)[0] 

    for script, (startBand, endBand) in _knownBands.iteritems():
        if startBand <= char <= endBand:
            return script
    else:
        return Script.Unknown

#----------------------------------------------------------------------------#

def scriptBoundaries(jString):
    u"""
    Determines where the script boundaries are in the given string.
        
    @param jString: The string of Japanese to segment.
    @type jString: string
    @return: A tuple of script-contiguous blocks
    """
    assert type(jString) == unicode
    segments = ()
    currentSegType = scriptType(jString[0])
    currentSeg = jString[0]
    for char in jString[1:]:
        if scriptType(char) == currentSegType or char == u'ー':
            currentSeg += char
        else:
            segments += currentSeg,

            currentSegType = scriptType(char)
            currentSeg = char
    else:
        if currentSeg:
            segments += currentSeg,
    
    return segments

#----------------------------------------------------------------------------#

def scriptTypes(jString):
    u"""
    Returns a set of the script types in the given string.
    """
    assert type(jString) == unicode
    return set(map(scriptType, jString))

#----------------------------------------------------------------------------#

def uniqueKanji(jString):
    u"""Returns the set of all unique kanji found in the given string."""
    kanjiSet = set(jString)
    for char in list(kanjiSet):
        if scriptType(char) != Script.Kanji:
            kanjiSet.remove(char)

    return kanjiSet

#----------------------------------------------------------------------------#

