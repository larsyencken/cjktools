# -*- coding: utf-8 -*-
#
#  cjkdata.py
#  cjktools
#

from os import path, environ

SEARCH_PATHS = [
    '~/.cjktools',
    '/usr/share/data/cjktools',
    '/usr/local/share/data/cjktools',
]


def find_path():
    if 'CJKTOOLS_DATA' in environ:
        return environ['CJKTOOLS_DATA']

    for p in SEARCH_PATHS:
        p = path.expanduser(p)
        if path.isdir(p):
            return p

    raise Exception('Please install the cjktools data pack and set the '
                    'CJKTOOLS_DATA environment variable')


def get_resource(name):
    base = find_path()
    return path.join(base, name)
