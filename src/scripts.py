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

_known_bands = {
        Script.Ascii:           (u'\u0021', u'\u00ff'),
        Script.Hiragana:	    (u'\u3041', u'\u3096'),
        Script.Katakana:	    (u'\u30a1', u'\u30f6'),
        Script.Kanji:	        (u'\u4e00', u'\u9fa5'),
        Script.FullAscii:	    (u'\uff01', u'\uff5f'),
        Script.HalfKatakana:    (u'\uff61', u'\uff9f'),
    }

_inter_kana_distance = 96

#----------------------------------------------------------------------------#

class ScriptMapping:
    """
    A mapping function between two scripts. We assume that the given scripts
    are different versions of the same characters, and further that they are
    aligned at the start and end points stored.
    """
    def __init__(self, from_script, to_script):
        """
        Constructor, initializes script conversion.
        
        @param from_script: The script to convert from.
        @type from_script: Script
        @param to_script: The script to convert to.
        @type to_script: Script
        """
        self.from_start, self.from_end = _known_bands[from_script]
        self.to_start, self.to_end = _known_bands[to_script]
        self.ord_diff = ord(self.to_start) - ord(self.from_start)
        assert (ord(self.from_end) - ord(self.from_start)) <= \
                (ord(self.to_end) - ord(self.to_start))
        return

    def __call__(self, j_string):
        """
        Converts any matching characters in the given string between scripts.
        Any characters which don't match the input script are passed through
        unchanged.
        """
        result = []
        for char in j_string:
            if self.from_start <= char <= self.from_end:
                result.append(unichr(ord(char) + self.ord_diff))
            else:
                result.append(char)

        return u''.join(result)

to_hiragana = ScriptMapping(Script.Katakana, Script.Hiragana)
to_katakana = ScriptMapping(Script.Hiragana, Script.Katakana)

#----------------------------------------------------------------------------#

_mapped_chars = {
            u'\u3000':  u'\u0020',
            u'\u3001':  u'\u002c',
            u'\u3002':  u'\u002e',
        }

_to_ascii = ScriptMapping(Script.FullAscii, Script.Ascii)

def normalize_ascii(j_string):
    """
    Normalize a double-width ascii string, converting all characters to
    their single-width counterparts.

    @param j_string: The string to convert.
    @type j_string: unicode
    @return: The converted string.
    """
    result = []
    for char in j_string:
        result.append(_mapped_chars.get(char, char))

    return _to_ascii(u''.join(result))

#----------------------------------------------------------------------------#

_full_width_kana = u"。「」、・ヲァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜"

def normalize_kana(j_string):
    """
    Normalizes all half-width katakana to normal width katakana. Leaves
    all other characters unchanged.

        >>> x = normalize_kana(unicode('ｶｷｸｹｺ', 'utf8'))
        >>> x == unicode('カキクケコ', 'utf8') 
        True

    @param j_string: The string to convert.
    @type j_string: unicode
    @return: The converted string.
    """
    start_h_w_kana, end_h_w_kana = _known_bands[Script.HalfKatakana]
    result = []
    for char in j_string:
        if start_h_w_kana <= char <= end_h_w_kana:
            result.append(_full_width_kana[ord(char) - 0xff61])
        else:
            result.append(char)

    return u''.join(result)

#----------------------------------------------------------------------------#

def normalize(j_string):
    """
    Jointly normalized full width ascii to single width ascii and half-width
    katakana to full with katakana.

        >>> x = normalize(unicode('Aあア阿ｱＡ', 'utf8'))
        >>> x == unicode('Aあア阿アA', 'utf8')
        True

    @param j_string: The string to convert.
    @type j_string: unicode
    @return: The converted string.
    """
    return normalize_ascii(normalize_kana(j_string))

#----------------------------------------------------------------------------#

def get_script(script):
    """
    Returns a string containing all charcters in the given script.
    """

    script_starts, script_ends = _known_bands[script]

    output = []
    for i in xrange(ord(script_starts), ord(script_ends) + 1):
        output.append(unichr(i))

    return ''.join(output)

#----------------------------------------------------------------------------#

def compare_kana(j_string_a, j_string_b):
    """
    Compares two kana strings in a script-independent manner.

        >>> ru_h = unicode('る', 'utf8')
        >>> ka_h = unicode('か', 'utf8')
        >>> ka_k = unicode('カ', 'utf8')
        >>> compare_kana(ru_h, ka_k) == cmp(ru_h, ka_h)
        True

    @type j_string_a: unicode
    @type j_string_b: unicode
    """
    return cmp(to_katakana(j_string_a), to_katakana(j_string_b))

#----------------------------------------------------------------------------#

def contains_script(script, j_string):
    """
    Returns True if the given script is within the string, False
    otherwise.
    
        >>> woof = u'woof'
        >>> contains_script(Script.Ascii, woof)
        True
        >>> contains_script(Script.Kanji, woof)
        False

    @param script: The script to search for.
    @type script: Script
    @param j_string: The string to search within.
    @type j_string: unicode
    """
    return script in script_types(j_string)

#----------------------------------------------------------------------------#

def script_type(char):
    """
    Determine the type of script contained in the given character. Script
    types are expressed using the Script enum.

        >>> woof = u'woof'
        >>> script_types(woof)
        set([Ascii])

        >>> beijing = unicode('北京', 'utf8')
        >>> script_types(beijing)
        set([Kanji])

        >>> ru = unicode('る', 'utf8')
        >>> script_types(ru)
        set([Hiragana])

    @param char: The character to examine.
    @type char: unicode
    @return: The script type.   
    """
    # Normalize/typecheck our input.
    char = unicode(char)[0] 

    for script, (start_band, end_band) in _known_bands.iteritems():
        if start_band <= char <= end_band:
            return script
    else:
        return Script.Unknown

#----------------------------------------------------------------------------#

def script_boundaries(j_string):
    """
    Determines where the script boundaries are in the given string.
        
        >>> taberu = unicode('食べる', 'utf8')
        >>> script_boundaries(taberu) == (taberu[0], taberu[1:])
        True

    @param j_string: The string of Japanese to segment.
    @type j_string: string
    @return: A tuple of script-contiguous blocks
    """
    assert type(j_string) == unicode
    segments = ()
    current_seg_type = script_type(j_string[0])
    current_seg = j_string[0]
    for char in j_string[1:]:
        if script_type(char) == current_seg_type or char == u'ー':
            current_seg += char
        else:
            segments += current_seg,

            current_seg_type = script_type(char)
            current_seg = char
    else:
        if current_seg:
            segments += current_seg,
    
    return segments

#----------------------------------------------------------------------------#

def script_types(j_string):
    """
    Returns a set of the script types in the given string.

        >>> woof = u'woof'
        >>> script_types(woof)
        set([Ascii])

        >>> beijing = unicode('北京', 'utf8')
        >>> script_types(beijing)
        set([Kanji])

        >>> taberu = unicode('食べる', 'utf8')
        >>> script_types(taberu)
        set([Hiragana, Kanji])
    """
    return set(map(script_type, j_string))

#----------------------------------------------------------------------------#

def unique_kanji(j_string):
    """
    Returns the set of all unique kanji found in the given string.

        >>> taberu = unicode('食べる', 'utf8')
        >>> unique_kanji(taberu) == set([taberu[0]])
        True
    """
    kanji_set = set(j_string)
    for char in list(kanji_set):
        if script_type(char) != Script.Kanji:
            kanji_set.remove(char)

    return kanji_set

#----------------------------------------------------------------------------#
