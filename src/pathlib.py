# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# pathlib.py
# Lars Yencken <lljy@csse.unimelb.edu.au>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Apr 26 16:27:36 2006
#
#----------------------------------------------------------------------------#

""" Path support for large projects, modelled on the pathconf module, but
    highly simplified.
"""

#----------------------------------------------------------------------------#

import os, sys
from os import path

#----------------------------------------------------------------------------#

_booted = False
_baseDir = None

#----------------------------------------------------------------------------#

def boot(relPathToBase):
    """ Ensures the base path is in the pythonPath.

        @param relPathToBase: The path from the booting module to the base
            directory for the project.
    """
    global _booted, _baseDir

    if _booted:
        return

    sys.path = map(path.abspath, sys.path)

    # swap slashes for whatever's the OS default
    relPathToBase = apply(path.join, relPathToBase.split('/'))

    # find current module directory
    moduleDir = path.dirname(path.abspath(sys.argv[0]))

    if moduleDir.startswith('/usr/bin') or \
            moduleDir.startswith('/usr/local/bin'):
        moduleDir = path.abspath(os.getcwd())

    # find the project base directory
    baseDir = path.normpath(path.join(moduleDir, relPathToBase))

    # add it to the front of sys.path
    sys.path[0:0] = [baseDir]

    _baseDir = baseDir
    _booted = True
    return

#----------------------------------------------------------------------------#

def getBaseDir():
    """ Get the base directory of the project.
    """
    global _booted, _baseDir

    if not _booted:
        raise Exception, "Project hasn't been booted yet."

    return _baseDir

#----------------------------------------------------------------------------#
