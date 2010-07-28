# -*- coding: utf-8 -*-
# 
#  zhuyin_table.py
#  foks
#  
#  Created by Lars Yencken on 2006-12-22.
#  Copyright 2006-2010 Lars Yencken. All rights reserved.
# 

"""
An interface to the zhuyin <-> pinyin table.
"""

#----------------------------------------------------------------------------#

import codecs
import pkg_resources

#----------------------------------------------------------------------------#

def _open_conversion_file():
    return codecs.getreader('utf8')(pkg_resources.resource_stream(
            'cjktools_data', 'tables/zhuyin_pinyin_conv_table'))

def get_zhuyin_to_pinyin_table():
    """Returns a dictionary mapping zhuyin to pinyin."""
    table = {}
    for zhuyin, pinyin in parse_lines(_open_conversion_file()):
        table[zhuyin] = pinyin

    return table
    
def parse_lines(stream):
    for line in stream:
        if not line.startswith('#'):
            yield line.rstrip().split()

#----------------------------------------------------------------------------#

def get_pinyin_to_zhuyin_table():
    """Returns a dictionary mapping zhuyin to pinyin."""    
    table = {}
    for zhuyin, pinyin in parse_lines(_open_conversion_file()):
        table[pinyin] = zhuyin

    return table

#----------------------------------------------------------------------------#

def pinyin_regex_pattern():
    """
    Returns a pinyin regex pattern, with optional tone number.
    """
    all_pinyin = ['r']

    for zhuyin, pinyin in parse_lines(_open_conversion_file()):
        all_pinyin.append(pinyin)

    # Sort from longest to shortest, so as to make maximum matches whenever
    # possible.
    all_pinyin.sort(lambda x, y: cmp(len(y), len(x)))

    # Build a generic pattern for a single pinyin with an optional tone.
    pattern = '(%s)([0-5]?)' % '|'.join(all_pinyin)

    return pattern

#----------------------------------------------------------------------------#

def zhuyin_regex_pattern():
    """
    Returns a zhuyin regex pattern.
    """
    all_pinyin = []

    for zhuyin, pinyin in parse_lines(_open_conversion_file()):
        all_pinyin.append(pinyin)

    pattern = '(%s)[0-4]?' % '|'.join(all_pinyin)

    return pattern

#----------------------------------------------------------------------------#
