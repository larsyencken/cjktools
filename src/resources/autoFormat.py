# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# autoFormat.py
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

def detectFormat(filename):
    """
    Reads the first line of the filename, and attempts to determine the
    format of the dictionary. The matching format is returned, or an
    UnknownFormatError is thrown.

    @param filename: The file to attempt to read.
    """
    global knownFormats

    iStream = sopen(filename, 'r')
    header = iStream.readline()
    iStream.close()

    for format in knownFormats:
        if format.matchHeader(header):
            return format
    else:
        raise UnknownFormatError, filename

#----------------------------------------------------------------------------#

def loadDictionary(filename):
    """
    Attempts to detect the format of and parse a dictionary, returning the
    dictionary object on success.
    """
    return detectFormat(filename).parseDictionary(filename)

#----------------------------------------------------------------------------#

def iterEntries(filename):
    """
    Iterates over dictionary entries, without storing them all in memory
    at once.
    """
    return detectFormat(filename).iterEntries(filename)

#----------------------------------------------------------------------------#
# DICTIONARY FORMATS
#----------------------------------------------------------------------------#

knownFormats = [
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

