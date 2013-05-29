# -*- coding: utf-8 -*-
#
#  zhuyin_table.py
#  cjktools
#

"""
An interface to the zhuyin <-> pinyin table.
"""

import codecs

import cjkdata


def _default_stream():
    return open(cjkdata.get_resource('tables/zhuyin_pinyin_conv_table'))


def zhuyin_to_pinyin_table(istream=None):
    "Returns a dictionary mapping zhuyin to pinyin."
    istream = istream or _default_stream()

    table = {}
    for zhuyin, pinyin in parse_lines(istream):
        table[zhuyin] = pinyin

    return table


def parse_lines(istream):
    istream = codecs.getreader('utf8')(istream)
    for line in istream:
        if not line.startswith('#'):
            yield line.rstrip().split()


def pinyin_to_zhuyin_table(istream=None):
    "Returns a dictionary mapping zhuyin to pinyin."
    istream = istream or _default_stream()
    table = {}
    for zhuyin, pinyin in parse_lines(istream):
        table[pinyin] = zhuyin

    return table


def pinyin_regex_pattern(istream=None):
    "Returns a pinyin regex pattern, with optional tone number."
    istream = istream or _default_stream()
    all_pinyin = ['r']

    for zhuyin, pinyin in parse_lines(istream):
        all_pinyin.append(pinyin)

    # Sort from longest to shortest, so as to make maximum matches whenever
    # possible.
    all_pinyin.sort(lambda x, y: cmp(len(y), len(x)))

    # Build a generic pattern for a single pinyin with an optional tone.
    pattern = '(%s)([0-5]?)' % '|'.join(all_pinyin)

    return pattern


def zhuyin_regex_pattern(istream=None):
    "Returns a zhuyin regex pattern."
    istream = istream or _default_stream()
    all_pinyin = []

    for zhuyin, pinyin in parse_lines(istream):
        all_pinyin.append(pinyin)

    pattern = '(%s)[0-4]?' % '|'.join(all_pinyin)

    return pattern
