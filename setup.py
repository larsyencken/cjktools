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

cjktoolsVersion = u'0.8a'
hgVersion = os.popen(u'hg parents').readlines()[0].rstrip()
hgVersion = re.sub(r'^changeset:\s*(\d+):[^\s]+$', r'\1', hgVersion)

setup(
        name='cjktools',
        version='%s.%s' % (cjktoolsVersion, hgVersion),
        package_dir={'cjktools': 'src'},
        packages=['cjktools', 'cjktools.dict'],
        scripts=['src/dyntest.py']
    )
