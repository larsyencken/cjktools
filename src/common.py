# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# common.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Feb 26 15:22:24 2007
#
#----------------------------------------------------------------------------#

"""
High-frequency, common tools. 
"""

#----------------------------------------------------------------------------#

import sys
import codecs
import bz2, gzip

#----------------------------------------------------------------------------#

def filterComments(fileStream):
    """
    Filter a filestream, removing comment lines marked with an initial
    hash.
    """
    for line in fileStream:
        if line.startswith('#'):
            continue

        yield line

    return

#----------------------------------------------------------------------------#

def smartLineIter(filenames, encoding='utf8'):
    """
    Returns an interator over the lines in the given files.

    @param filenames: A sequence of files whose lines to iterate over.
    @param encoding: The encoding to use [utf8]
    """
    for filename in filenames:
        iStream = sopen(filename, 'r', encoding)
        for line in iStream:
            yield line
        iStream.close()

    return

#----------------------------------------------------------------------------#

def sopen(filename, mode='rb', encoding='utf8'):
    """
    Transparently uses compression on the given file based on file
    extension.

    @param filename: The filename to use for the file handle.
    @param mode: The mode to open the file in, e.g. 'r' for read, 'w' for
        write, 'a' for append.
    @param encoding: The encoding to use. Can be set to None to avoid
        using unicode at all.
    """
    readMode = 'r' in mode
    if readMode and 'w' in mode:
        raise Exception, "Must be either read mode or write, but not both"

    if filename.endswith('.bz2'):
        stream = bz2.BZ2File(filename, mode)
    elif filename.endswith('.gz'):
        stream = gzip.GzipFile(filename, mode)
    elif filename == '-':
        if readMode:
            stream = sys.stdin
        else:
            stream = sys.stdout
    else:
        stream = open(filename, mode)
    
    if encoding not in (None, 'byte'):
        if readMode:
            return codecs.getreader(encoding)(stream)
        else:
            return codecs.getwriter(encoding)(stream)
    
    return stream

#----------------------------------------------------------------------------#

