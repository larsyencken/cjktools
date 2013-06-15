# -*- coding: utf-8 -*-
#
#  cjkdata.py
#  cjktools
#

from os import path, environ

SEARCH_PATHS = [
    '~/.cjkdata',
    '/usr/share/data/cjkdata',
    '/usr/local/share/data/cjkdata',
]


def find_path():
    if 'CJKDATA' in environ:
        return environ['CJKDATA']

    for p in SEARCH_PATHS:
        p = path.expanduser(p)
        if path.isdir(p):
            return p

    raise Exception('Please install the cjk data pack and set the '
                    'CJKDATA environment variable')


def get_resource(name):
    base = find_path()
    return path.join(base, name)
