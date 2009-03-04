# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# zhuyinTable.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Fri Dec 22 16:05:44 2006
#
#----------------------------------------------------------------------------#

"""
An interface to the zhuyin <-> pinyin table.
"""

#----------------------------------------------------------------------------#

import os, re
import cjktools.common
from cjktools.common import sopen
from cjktools.table import parseLines 
import settings

#----------------------------------------------------------------------------#

def getConversionFile():
    return os.path.join(settings.getDataDir(), 'tables',
            'zhuyin_pinyin_conv_table')

#----------------------------------------------------------------------------#

def getZhuyinToPinyinTable():
    """Returns a dictionary mapping zhuyin to pinyin."""
    table = {}
    for zhuyin, pinyin in parseLines(sopen(getConversionFile())):
        table[zhuyin] = pinyin

    return table

#----------------------------------------------------------------------------#

def getPinyinToZhuyinTable():
    """Returns a dictionary mapping zhuyin to pinyin."""    
    table = {}
    for zhuyin, pinyin in parseLines(sopen(getConversionFile())):
        table[pinyin] = zhuyin

    return table

#----------------------------------------------------------------------------#

def pinyinRegexPattern():
    """
    Returns a pinyin regex pattern, with optional tone number.
    """
    allPinyin = ['r']

    for zhuyin, pinyin in parseLines(sopen(getConversionFile())):
        allPinyin.append(pinyin)

    # Sort from longest to shortest, so as to make maximum matches whenever
    # possible.
    allPinyin.sort(lambda x, y: cmp(len(y), len(x)))

    # Build a generic pattern for a single pinyin with an optional tone.
    pattern = '(%s)([0-5]?)' % '|'.join(allPinyin)

    return pattern

#----------------------------------------------------------------------------#

def zhuyinRegexPattern():
    """
    Returns a zhuyin regex pattern.
    """
    allPinyin = []

    for zhuyin, pinyin in parseLines(sopen(getConversionFile())):
        allPinyin.append(pinyin)

    pattern = '(%s)[0-4]?' % '|'.join(allPinyin)

    return pattern

#----------------------------------------------------------------------------#
