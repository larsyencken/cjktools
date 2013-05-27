# -*- coding: utf-8 -*-
#
#  kanji_list.py
#  cjktools
#

"""
An interface to the kanji lists.
"""

import pkg_resources

from cjktools import scripts


def get_lists():
    """
    Returns list containing the names of all existing kanji lists.
    """
    result = []
    for filename in pkg_resources.resource_listdir('cjktools_data',
                                                   'lists/char'):
        result.append(filename)

    return result


def get_list(list_name):
    """
    Returns the kanji in the given list.
    """
    s = pkg_resources.resource_string('cjktools_data',
                                      'lists/char/%s' % list_name)
    return scripts.unique_kanji(s.decode('utf8'))
