# -*- coding: utf-8 -*-
#
#  Utilities common to many test files.
#
#  cjktools.tests._common.py
#

import codecs

from six.moves import StringIO
from six import binary_type

def to_unicode_stream(x):
    o = StringIO(x)

    if isinstance(x, binary_type):
        o = codecs.getreader('utf8')(o)

    return o