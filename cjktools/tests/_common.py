# -*- coding: utf-8 -*-
#
#  Utilities common to many test files.
#
#  cjktools.tests._common.py
#

import codecs

from six.moves import StringIO
from six import binary_type, text_type
from six import PY2

def to_unicode_stream(x):
    o = StringIO(x)

    if isinstance(x, binary_type):
        o = codecs.getreader('utf8')(o)

    return o

def to_string_stream(x):
    """
    For modules that require a encoding as ``str`` in both Python 2 and
    Python 3, we can't just encode automatically. 
    """
    if PY2 and isinstance(x, text_type):
        x = x.encode('utf-8')

    return StringIO(x)

