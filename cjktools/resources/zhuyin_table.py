# -*- coding: utf-8 -*-
#
#  zhuyin_table.py
#  cjktools
#

"""
An interface to the zhuyin <-> pinyin table.
"""

import codecs

from six import PY2

from . import cjkdata
from cjktools.common import _NullContextWrapper as NullContextWrapper


def _default_stream():
    return open(cjkdata.get_resource('tables/zhuyin_pinyin_conv_table'))

def _get_stream_context(istream=None):
    """
    If passed a stream, return a context that does not affect that stream's
    context when passed to a ``with`` statement. If no stream is passed,
    this passes the (opened) default stream.
    """
    if istream is None:
        return _default_stream()
    else:
        return NullContextWrapper(istream)


def parse_lines(istream):
    # TODO: Come up with a more elegant way to handle this
    if PY2:
        istream = codecs.getreader('utf8')(istream)

    for line in istream:
        if not line.startswith('#'):
            yield line.rstrip().split()


def zhuyin_to_pinyin_table(istream=None):
    """Returns a dictionary mapping zhuyin to pinyin."""
    with _get_stream_context(istream) as stream:
        table = {}
        for zhuyin, pinyin in parse_lines(stream):
            table[zhuyin] = pinyin

    return table


def pinyin_to_zhuyin_table(istream=None):
    "Returns a dictionary mapping zhuyin to pinyin."
    with _get_stream_context(istream):
        table = {}
        for zhuyin, pinyin in parse_lines(istream):
            table[pinyin] = zhuyin

    return table


def pinyin_regex_pattern(istream=None):
    "Returns a pinyin regex pattern, with optional tone number."
    with _get_stream_context(istream):
        all_pinyin = ['r']

        for zhuyin, pinyin in parse_lines(istream):
            all_pinyin.append(pinyin)

    # Sort from longest to shortest, so as to make maximum matches whenever
    # possible.
    all_pinyin = sorted(all_pinyin, key=len)

    # Build a generic pattern for a single pinyin with an optional tone.
    pattern = '(%s)([0-5]?)' % '|'.join(all_pinyin)

    return pattern


def zhuyin_regex_pattern(istream=None):
    "Returns a zhuyin regex pattern."
    with _get_stream_context(istream):
        all_pinyin = []

        for zhuyin, pinyin in parse_lines(istream):
            all_pinyin.append(pinyin)

    pattern = '(%s)[0-4]?' % '|'.join(all_pinyin)

    return pattern
