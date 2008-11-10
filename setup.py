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

from distutils.core import setup
import os
import re

#----------------------------------------------------------------------------#

def get_hg_version():
    version = None
    if os.system('which hg >/dev/null 2>/dev/null') == 0:
        version = os.popen('hg id -n 2>/dev/null').read().strip():
    return version or 'unknown'

cjktoolsVersion = u'0.9'

setup(
        name='python-cjktools',
        version='%s.%s' % (cjktoolsVersion, get_hg_version()),
        package_dir={'cjktools': 'src'},
        packages=['cjktools', 'cjktools.resources'],
        scripts=['src/dyntest.py']
    )
