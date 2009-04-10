# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# kanji_list.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 12 19:18:19 2006
#
#----------------------------------------------------------------------------#

"""
An interface to the kanji lists.
"""

#----------------------------------------------------------------------------#

import os
import pkg_resources

from cjktools.common import sopen
from cjktools import scripts

#----------------------------------------------------------------------------#

def get_lists():
    """
    Returns list containing the names of all existing kanji lists.
    """
    result = []
    for filename in pkg_resources.resource_listdir('cjktools_data',
            'lists/char'):
        result.append(filename)

    return result

#----------------------------------------------------------------------------#

def get_list(list_name):
    """
    Returns the kanji in the given list.
    """
    return scripts.unique_kanji(pkg_resources.resource_string('cjktools_data', 
            'lists/char/%s' % list_name).decode('utf8'))

#----------------------------------------------------------------------------#
