# -*- coding: utf-8 -*-
#
#  scripts.py
#  cjktools
#

"""
This module is responsible for Japanese script/encoding specific methods,
especially determining the script type of an entry. It is thus the only
module which requires a utf8 encoding for the additional Japanese characters.
"""
from __future__ import unicode_literals

from six import unichr, text_type, iteritems
from six.moves import range


class Script:
    Hiragana = 1
    Katakana = 2
    Kanji = 3
    Ascii = 4
    FullAscii = 5
    HalfKatakana = 6
    Unknown = 7

_known_bands = {
    Script.Ascii:           ('\u0021', '\u00ff'),
    Script.Hiragana:	    ('\u3041', '\u3096'),
    Script.Katakana:	    ('\u30a1', '\u30f6'),
    Script.Kanji:	        ('\u4e00', '\u9fa5'),
    Script.FullAscii:	    ('\uff01', '\uff5f'),
    Script.HalfKatakana:    ('\uff61', '\uff9f'),
}

_inter_kana_distance = 96


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
        assert ((ord(self.from_end) - ord(self.from_start)) <=
                (ord(self.to_end) - ord(self.to_start)))

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

        return ''.join(result)

to_hiragana = ScriptMapping(Script.Katakana, Script.Hiragana)
to_katakana = ScriptMapping(Script.Hiragana, Script.Katakana)


_mapped_chars = {
    '\u3000':  '\u0020',
    '\u3001':  '\u002c',
    '\u3002':  '\u002e',
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

    return _to_ascii(''.join(result))


_full_width_kana = "。「」、・ヲァィゥェォャュョッーアイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワン゛゜"  # nopep8


def normalize_kana(j_string):
    """
    Normalizes all half-width katakana to normal width katakana. Leaves
    all other characters unchanged.

        >>> x = normalize_kana(u'ｶｷｸｹｺ')
        >>> x == u'カキクケコ'
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

    return ''.join(result)


def normalize(j_string):
    """
    Jointly normalized full width ascii to single width ascii and half-width
    katakana to full with katakana.

        >>> x = normalize(u'Aあア阿ｱＡ')
        >>> x == u'Aあア阿アA'
        True

    @param j_string: The string to convert.
    @type j_string: unicode
    @return: The converted string.
    """
    return normalize_ascii(normalize_kana(j_string))


def get_script(script):
    """
    Returns a string containing all charcters in the given script.
    """

    script_starts, script_ends = _known_bands[script]

    output = []
    for i in range(ord(script_starts), ord(script_ends) + 1):
        output.append(unichr(i))

    return ''.join(output)


def compare_kana(j_string_a, j_string_b):
    """
    Compares two kana strings in a script-independent manner.

        >>> ru_h = u'る'
        >>> ka_h = u'か'
        >>> ka_k = u'カ'
        >>> compare_kana(ru_h, ka_k) == cmp(ru_h, ka_h)
        True

    @type j_string_a: unicode
    @type j_string_b: unicode
    """
    a = to_katakana(j_string_a)
    b = to_katakana(j_string_b)

    return (a > b) - (a < b)


def contains_script(script, j_string):
    """
    Returns True if the given script is within the string, False
    otherwise.

        >>> woof = 'woof'
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


def script_type(char):
    """
    Determine the type of script contained in the given character. Script
    types are expressed using the Script enum.

        >>> woof = 'woof'
        >>> script_types(woof)
        set([Ascii])

        >>> beijing = u'北京'
        >>> script_types(beijing)
        set([Kanji])

        >>> ru = u'る'
        >>> script_types(ru)
        set([Hiragana])

    @param char: The character to examine.
    @type char: unicode
    @return: The script type.
    """
    # Normalize/typecheck our input.
    if not len(char):
        return Script.Unknown

    char = text_type(char)[0]

    for script, (start_band, end_band) in iteritems(_known_bands):
        if start_band <= char <= end_band:
            return script
    else:
        return Script.Unknown


def script_boundaries(j_string):
    """
    Determines where the script boundaries are in the given string.

        >>> taberu = u'食べる'
        >>> script_boundaries(taberu) == (taberu[0], taberu[1:])
        True

    @param j_string: The string of Japanese to segment.
    @type j_string: string
    @return: A tuple of script-contiguous blocks
    """
    if not len(j_string):
        return (j_string, )

    assert isinstance(j_string, text_type)
    segments = ()
    current_seg_type = script_type(j_string)
    current_seg = j_string[0]
    for char in j_string[1:]:
        if script_type(char) == current_seg_type or char == 'ー':
            current_seg += char
        else:
            segments += current_seg,

            current_seg_type = script_type(char)
            current_seg = char
    else:
        if current_seg:
            segments += current_seg,

    return segments


def script_types(j_string):
    """
    Returns a set of the script types in the given string.

        >>> woof = 'woof'
        >>> script_types(woof)
        set([Ascii])

        >>> beijing = u'北京'
        >>> script_types(beijing)
        set([Kanji])

        >>> taberu = u'食べる'
        >>> script_types(taberu)
        set([Hiragana, Kanji])
    """
    return set(map(script_type, j_string))


def unique_kanji(j_string):
    """
    Returns the set of all unique kanji found in the given string.

        >>> taberu = u'食べる'
        >>> unique_kanji(taberu) == set([taberu[0]])
        True
    """
    kanji_set = set(j_string)
    for char in list(kanji_set):
        if script_type(char) != Script.Kanji:
            kanji_set.remove(char)

    return kanji_set
