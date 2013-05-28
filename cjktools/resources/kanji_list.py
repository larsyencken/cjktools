# -*- coding: utf-8 -*-
#
#  kanji_list.py
#  cjktools
#

"""
An interface to the kanji lists.
"""

import os
import codecs

from cjktools import scripts

import cjkdata


def get_lists():
    "Returns list containing the names of all existing kanji lists."
    return os.listdir(cjkdata.get_resource('lists/char'))


def get_list(list_name):
    "Returns the kanji in the given list."
    f = cjkdata.get_resource('lists/char/%s' % list_name)
    with codecs.open(f, 'r', 'utf8') as istream:
        return scripts.unique_kanji(istream.read())
