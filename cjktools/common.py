# -*- coding: utf-8 -*-
#
#  common.py
#  cjktools
#

"""
High-frequency, common tools.
"""

import sys
import codecs
import bz2
import gzip

import six


def filter_comments(file_stream):
    """
    Filter a filestream, removing comment lines marked with an initial hash.
    """
    for line in file_stream:
        if line.startswith('#'):
            continue

        yield line


def sopen(filename, mode='rb', encoding='utf8'):
    """
    Transparently uses compression on the given file based on file
    extension.

    :param filename:
        The filename to use for the file handle.
    
    :param mode:
        The mode to open the file in, e.g. ``'r'`` for read, ``'w'`` for
        write, ``'a'`` for append.
    
    :param encoding:
        The encoding to use. Can be set to None to avoid
        using unicode at all.
    """
    read_mode = 'r' in mode
    if read_mode and 'w' in mode:
        raise Exception("Must be either read mode or write, but not both")

    # Do this before any streams are opened to hopefully minimize the potential
    # for failing while resources are open.
    if encoding not in (None, 'byte') and six.PY2:
        if read_mode:
            streamhandler = codecs.getreader(encoding)
        else:
            streamhandler = codecs.getwriter(encoding)
    else:
        streamhandler = lambda x: x

    if filename.endswith('.bz2'):
        stream = bz2.BZ2File(filename, mode)
    elif filename.endswith('.gz'):
        stream = gzip.GzipFile(filename, mode)
    elif filename == '-':
        if read_mode:
            stream = sys.stdin
        else:
            stream = sys.stdout
    else:
        stream = open(filename, mode)

    return streamhandler(stream)


def stream_codec(istream):
    """
    Handles the common case where, in Python 2.x the stream needs decoding, but
    in Python 3.x it's doesn't.
    """
    # TODO: Find a more elegant way to do this
    if six.PY2:
        return codecs.getreader('utf8')(istream)

    return istream


def get_stream_context(default_stream_func, istream=None):
    if istream is None:
        return default_stream_func()
    else:
        return _NullContextWrapper(istream)


class _NullContextWrapper(object):
    """
    Class for wrapping contexts so that they are passed through in a
    with statement.
    """
    def __init__(self, context):
        self.context = context

    def __enter__(self):
        return self.context

    def __exit__(*args, **kwargs):
        pass

# If contextlib's ExitStack doesn't work, we need to pull it in from a backport
try:
    from contextlib import ExitStack as _ExitStack
except ImportError:
    from contextlib2 import ExitStack as _ExitStack
