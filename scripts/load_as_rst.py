#!/usr/bin/env python
"""
Used to convert Markdown files to RST for use in sphinx and PyPi.
"""
from __future__ import print_function

import os
import sys
import warnings

# This is called during setup, so we can't be sure six is installed.
# The only thing to pull in is raise_from, though, so we'll just warn
# about the missing exception chain if it's not installed.
try:
    from six import raise_from
except ImportError:
    warnings.warn('six not found: Exception chaining will not be used in '
                  'python 3', ImportWarning)    
    def raise_from(value, from_value):
        raise value

# See https://stackoverflow.com/a/23265673/467366 for general approach
def _fallback_load(fname, strict=False, parent_exception=None):
        failure_msg = ('pypandoc module not available, returning text in its '
                       'original format')
        if strict and parent_exception is not None:
            raise raise_from(ImportError(failure_msg), parent_exception)
        else:
            warnings.warn(failure_msg, ImportWarning)

        with open(fname, 'r') as f:
            return f.read()

try:
    from pypandoc import convert as pypandoc_convert
    def load_text(fname, strict=False):
        try:
            return pypandoc_convert(fname, 'rst')
        except (ImportError, OSError) as e:
            return _fallback_load(fname, strict=strict, parent_exception=e)
except ImportError as e:
    __err = e
    def load_text(fname, strict=False):
        return _fallback_load(fname, strict=strict, parent_exception=__err)


def convert(fname_in, fname_out=None, preamble=None, strict=False):
    """
    Converts an file at ``fname_in`` from a format understood by pypandoc
    to ReStructuredText.

    :param fname_in:
        Filename to read.

    :param fname_out:
        Filename to write to - this will be overwritten. If unspecified,
        the converted text is returned.

    :param preamble:
        A preamble to add to the file (e.g. "#This is an auto-generated file")
    """
    if fname_in is None:
        raise ValueError('Must specify an input file')

    if not os.path.exists(fname_in):
        raise IOError('File not found: {}'.format(fname_in))

    text = preamble or ''
    text = '\n'.join((text, load_text(fname_in, strict=strict)))

    if fname_out is not None:
        with open(fname_out, 'w') as f:
            print(text, file=f)

        return None         # Just being explicit
    else:
        return text


if __name__ == "__main__":
    import argparse
    import os

    desc = ('Loads a file supported by pypandoc as RST and outputs it to '
            'either the stdout or a specified file.')
    parser = argparse.ArgumentParser(desc)

    parser.add_argument('input', type=str, default=None,
                        help='The file to convert to RST.')

    parser.add_argument('-o', '--output', type=str, default=None,
                        help=('The file to which to output the converted text '
                              '(Warning: this will be overwritten if exists)'))

    args = parser.parse_args()

    output = convert(args.input, args.output)
    if output is not None:
        print(output)

