# -*- coding: utf-8 -*-
#
#  auto_format.py
#  cjktools
#

"""
A module of methods to automatically detect the format given a dictionary
file.
"""
from __future__ import unicode_literals

from .dict_format import RegexFormat, UnknownFormatError


def detect_format(header):
    """
    Reads the first line of the filename, and attempts to determine the
    format of the dictionary. The matching format is returned, or an
    UnknownFormatError is thrown.
    """
    for f in known_formats:
        if f.match_header(header):
            return f

    raise UnknownFormatError('unknown header line: %s' % repr(header))


def load_dictionary(istream):
    """
    Attempts to detect the format of and parse a dictionary, returning the
    dictionary object on success.
    """
    lines = iter(istream)
    header = next(lines)
    return detect_format(header).parse_dictionary(lines)


def iter_entries(istream):
    """
    Iterates over dictionary entries, without storing them all in memory
    at once.
    """
    lines = iter(istream)
    header = next(lines)
    return detect_format(header).iter_entries(lines)

#----------------------------------------------------------------------------#
# DICTIONARY FORMATS
#----------------------------------------------------------------------------#

known_formats = [
    RegexFormat(
        'edict',
        '^.？？？.*$',
        '^(?P<word>[^ ]+) (\[(?P<reading>[^\]]+)\] )?(?P<senses>.*)$',
        '/(?P<sense>[^/]+)',
    ),
    RegexFormat(
        'jc_kdic',
        '^FORMAT jc_kdic$',
        '^(?P<word>[^ ]+) \[(?P<reading>[^\]]+)\]\t(?P<senses>.*)$',
        '(?P<sense>[^，]+)[，]?',
    ),
    RegexFormat(
        'cj_kdic',
        '^FORMAT cj_kdic$',
        '^(?P<word>[^\t]+)\t(?P<reading>[^\\\\]+)\\\\n(?P<senses>.*)$',
        '([１２３４５７８９０]+．)?(?P<sense>[^\\\\]+)(\\\\n)?',
    ),
    RegexFormat(
        'cedict',
        '^# CEDICT.*$',
        '^[^ ]+ (?P<word>[^ ]+) (\[(?P<reading>[^\]]+)\])?(?P<senses>.*)',
        '/(?P<sense>[^/]+)',
    ),
]
