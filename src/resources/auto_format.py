# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# auto_format.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 26 13:55:56 2006
#
#----------------------------------------------------------------------------#

"""
A module of methods to automatically detect the format given a dictionary
file.
"""

#----------------------------------------------------------------------------#

import os

from cjktools.common import sopen

from format import RegexFormat
import languages

#----------------------------------------------------------------------------#

def detect_format(filename):
    """
    Reads the first line of the filename, and attempts to determine the
    format of the dictionary. The matching format is returned, or an
    UnknownFormatError is thrown.

    @param filename: The file to attempt to read.
    """
    global known_formats

    i_stream = sopen(filename, 'r')
    header = i_stream.readline()
    i_stream.close()

    for format in known_formats:
        if format.match_header(header):
            return format
    else:
        raise UnknownFormatError, filename

#----------------------------------------------------------------------------#

def load_dictionary(filename):
    """
    Attempts to detect the format of and parse a dictionary, returning the
    dictionary object on success.
    """
    return detect_format(filename).parse_dictionary(filename)

#----------------------------------------------------------------------------#

def iter_entries(filename):
    """
    Iterates over dictionary entries, without storing them all in memory
    at once.
    """
    return detect_format(filename).iter_entries(filename)

#----------------------------------------------------------------------------#
# DICTIONARY FORMATS
#----------------------------------------------------------------------------#

known_formats = [
        RegexFormat('edict',
                u'^？？？？.*$',
                u'^(?P<word>[^ ]+) (\[(?P<reading>[^\]]+)\] )?(?P<senses>.*)$',
                u'/(?P<sense>[^/]+)',
            ),
        RegexFormat('jc_kdic',
                u'^FORMAT jc_kdic$',
                u'^(?P<word>[^ ]+) \[(?P<reading>[^\]]+)\]\t(?P<senses>.*)$',
                u'(?P<sense>[^，]+)[，]?',
            ),
        RegexFormat('cj_kdic',
                u'^FORMAT cj_kdic$',
                u'^(?P<word>[^\t]+)\t(?P<reading>[^\\\\]+)\\\\n(?P<senses>.*)$',
                u'([１２３４５７８９０]+．)?(?P<sense>[^\\\\]+)(\\\\n)?',
            ),
        RegexFormat('cedict',
                u'^# CEDICT.*$',
                u'^[^ ]+ (?P<word>[^ ]+) (\[(?P<reading>[^\]]+)\])?(?P<senses>.*)',
                u'/(?P<sense>[^/]+)',
            ),
    ]

#----------------------------------------------------------------------------#

