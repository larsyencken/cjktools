# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# setup.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Jun 27 12:30:37 2007
#
#----------------------------------------------------------------------------#

"""
Package setup file for the jptools package.
"""

#----------------------------------------------------------------------------#

from distutils.core import setup
import os

#----------------------------------------------------------------------------#

jptoolsVersion = u'0.8a'
hgVersion = os.popen(u'hg id').read().replace(u' ', u'_')

setup(
        name='jptools',
        version='%s:%s' % (jptoolsVersion, hgVersion),
        package_dir={'jptools': 'src'},
        packages=['jptools'],
        scripts=['src/dyntest.py']
    )
