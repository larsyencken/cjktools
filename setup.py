# -*- coding: utf-8 -*-
#
#  setup.py
#  cjktools
#

"""
Package setup file for the cjktools package.
"""

import sys
from setuptools import setup

from scripts.load_as_rst import convert

try:
    from setuptools_scm import get_version

    VERSION = get_version()

    f = open('cjktools/__version__.py', 'w')
    f.write('# Autogenerated by setup.py\n')
    f.write('version = "%s"\n' % VERSION)
    f.close()
except ImportError:
    pass

LONG_DESCRIPTION = convert('README.md', strict=False)

# For Python <= 3.4, we need to pull in the backport of enum
REQUIRES = ['six']
if sys.version_info < (3, 4, 0):
    REQUIRES.append('enum34')

# For Python <= 3.3 we need to pull in the backport of ExitStack
if sys.version_info < (3, 3, 0):
    REQUIRES.append('contextlib2')

# Set up the classifiers
CLASSIFIERS = [
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

setup(
    name='cjktools',
    description="A library for basic CJK processing and lexicography.",
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    url="https://github.com/larsyencken/cjktools",
    author="Lars Yencken",
    author_email="lars@yencken.org",
    license="BSD",
    install_requires=REQUIRES,
    package_dir={'cjktools': 'cjktools'},
    packages=['cjktools', 'cjktools.resources'],
    test_suite='cjktools.tests',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
)
