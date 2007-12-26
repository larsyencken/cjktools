# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# __init__.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Sun May 15 23:12:04 EST 2005
#
#----------------------------------------------------------------------------#

"""
This module is responsible for Japanese script/encoding specific methods,
especially determining the script type of an entry. It is thus the only
module which requires a utf8 encoding for the additional Japanese characters.
"""

#----------------------------------------------------------------------------#

import enum

#----------------------------------------------------------------------------#
# CONSTANTS
#----------------------------------------------------------------------------#

Script = enum.Enum(u'Hiragana', u'Katakana', u'Kanji', u'Ascii',
        u'FullAscii', u'HalfKatakana', u'Unknown')

_knownBands = {
        Script.Ascii:           (u'\u0021', u'\u00ff'),
        Script.Hiragana:	    (u'\u3041', u'\u3096'),
        Script.Katakana:	    (u'\u30a1', u'\u30f6'),
        Script.Kanji:	        (u'\u4e00', u'\u9fa5'),
        Script.FullAscii:	    (u'\uff01', u'\uff5f'),
        Script.HalfKatakana:    (u'\uff61', u'\uff9f'),
    }

_interKanaDistance = 96

#----------------------------------------------------------------------------#

class ScriptMapping:
    """
    A mapping function between two scripts. We assume that the given scripts
    are different versions of the same characters, and further that they are
    aligned at the start and end points stored.
    """
    def __init__(self, fromScript, toScript):
        """
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
        """
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
    """
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

_fullWidthKana = u"。「」、・ヲァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜"

def normalizeKana(jString):
    """
    Normalizes all half-width katakana to normal width katakana. Leaves
    all other characters unchanged.

        >>> x = normalizeKana(unicode('ｶｷｸｹｺ', 'utf8'))
        >>> x == unicode('カキクケコ', 'utf8') 
        True

    @param jString: The string to convert.
    @type jString: unicode
    @return: The converted string.
    """
    startHWKana, endHWKana = _knownBands[Script.HalfKatakana]
    result = []
    for char in jString:
        if startHWKana <= char <= endHWKana:
            result.append(_fullWidthKana[ord(char) - 0xff61])
        else:
            result.append(char)

    return u''.join(result)

#----------------------------------------------------------------------------#

def normalize(jString):
    """
    Jointly normalized full width ascii to single width ascii and half-width
    katakana to full with katakana.

        >>> x = normalize(unicode('Aあア阿ｱＡ', 'utf8'))
        >>> x == unicode('Aあア阿アA', 'utf8')
        True

    @param jString: The string to convert.
    @type jString: unicode
    @return: The converted string.
    """
    return normalizeAscii(normalizeKana(jString))

#----------------------------------------------------------------------------#

def getScript(script):
    """
    Returns a string containing all charcters in the given script.
    """

    scriptStarts, scriptEnds = _knownBands[script]

    output = []
    for i in xrange(ord(scriptStarts), ord(scriptEnds) + 1):
        output.append(unichr(i))

    return ''.join(output)

#----------------------------------------------------------------------------#

def compareKana(jStringA, jStringB):
    """
    Compares two kana strings in a script-independent manner.

        >>> ru_h = unicode('る', 'utf8')
        >>> ka_h = unicode('か', 'utf8')
        >>> ka_k = unicode('カ', 'utf8')
        >>> compareKana(ru_h, ka_k) == cmp(ru_h, ka_h)
        True

    @type jStringA: unicode
    @type jStringB: unicode
    """
    return cmp(toKatakana(jStringA), toKatakana(jStringB))

#----------------------------------------------------------------------------#

def containsScript(script, jString):
    """
    Returns True if the given script is within the string, False
    otherwise.
    
        >>> woof = u'woof'
        >>> containsScript(Script.Ascii, woof)
        True
        >>> containsScript(Script.Kanji, woof)
        False

    @param script: The script to search for.
    @type script: Script
    @param jString: The string to search within.
    @type jString: unicode
    """
    return script in scriptTypes(jString)

#----------------------------------------------------------------------------#

def scriptType(char):
    """
    Determine the type of script contained in the given character. Script
    types are expressed using the Script enum.

        >>> woof = u'woof'
        >>> scriptTypes(woof)
        set([Ascii])

        >>> beijing = unicode('北京', 'utf8')
        >>> scriptTypes(beijing)
        set([Kanji])

        >>> ru = unicode('る', 'utf8')
        >>> scriptTypes(ru)
        set([Hiragana])

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
    """
    Determines where the script boundaries are in the given string.
        
        >>> taberu = unicode('食べる', 'utf8')
        >>> scriptBoundaries(taberu) == (taberu[0], taberu[1:])
        True

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
    """
    Returns a set of the script types in the given string.

        >>> woof = u'woof'
        >>> scriptTypes(woof)
        set([Ascii])

        >>> beijing = unicode('北京', 'utf8')
        >>> scriptTypes(beijing)
        set([Kanji])

        >>> taberu = unicode('食べる', 'utf8')
        >>> scriptTypes(taberu)
        set([Hiragana, Kanji])
    """
    return set(map(scriptType, jString))

#----------------------------------------------------------------------------#

def uniqueKanji(jString):
    """
    Returns the set of all unique kanji found in the given string.

        >>> taberu = unicode('食べる', 'utf8')
        >>> uniqueKanji(taberu) == set([taberu[0]])
        True
    """
    kanjiSet = set(jString)
    for char in list(kanjiSet):
        if scriptType(char) != Script.Kanji:
            kanjiSet.remove(char)

    return kanjiSet

#----------------------------------------------------------------------------#
