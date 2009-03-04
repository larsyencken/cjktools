# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# setup.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Jun 27 12:30:37 2007
#
#----------------------------------------------------------------------------#

"""
Package setup file for the cjktools package.
"""

#----------------------------------------------------------------------------#

from setuptools import setup
import os
import re

#----------------------------------------------------------------------------#

def get_hg_version():
    version = None
    if os.system('which hg >/dev/null 2>/dev/null') == 0:
        version = os.popen('hg id -n 2>/dev/null').read().strip().rstrip('+')
    return version or 'unknown'

cjktoolsVersion = u'1.1dev'

setup(
        name='cjktools',
        description="A library for basic CJK processing and lexicography.",
        long_description = """
        Provides basic script detection, manipulation of kana and interfaces
        for the popular EDICT and KANJIDIC families of dictionaries.
        """,
        url="http://bitbucket.org/lars512/cjktools/",
        version='%s.r%s' % (cjktoolsVersion, get_hg_version()),
        author="Lars Yencken",
        author_email="lljy@csse.unimelb.edu.au",
        license="BSD",

        package_dir={'cjktools': 'src'},
        packages=['cjktools', 'cjktools.resources'],
        scripts=['src/dyntest.py'],
    )
