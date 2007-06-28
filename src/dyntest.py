#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# dyntest.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Thu Oct 19 13:00:34 JST 2006
#
#----------------------------------------------------------------------------#

"""
A module with dynamic testing abilities. Is able to automatically generate
a suite of unit tests based on the current folder and subdirectories.
"""

#----------------------------------------------------------------------------#

import os, sys, optparse, codecs
import unittest

#----------------------------------------------------------------------------#
# PUBLIC METHODS
#----------------------------------------------------------------------------#

def dynamicSuite(rootDirectory, excludes=[]):
    """
    Generates a dynamic test suite out of the given directory.
    """
    # Change to the original directory.
    originalDir = os.getcwd()
    rootDirectory = os.path.abspath(rootDirectory)
    os.chdir(rootDirectory)
    if rootDirectory not in sys.path:
        sys.path.append(rootDirectory)

    suites = []
    for dirPath, filenames in _pythonWalk('.', excludes):
        importPath = dirPath.lstrip('.').split('/')[1:]

        for filename in filenames:
            if filename.startswith('test') and filename.endswith('.py'):
                # Import this test module.
                moduleName = filename[:-len('.py')]
                fullImportPath = importPath + [moduleName]

                module = __import__('.'.join(fullImportPath))

                if importPath:
                    # Need to fetch the submodule
                    for subModule in fullImportPath[1:]:
                        module = getattr(module, subModule)

                suites.append(module.suite())
    
    # Change back to the dir when this was called.
    os.chdir(originalDir)

    return unittest.TestSuite(suites)

#----------------------------------------------------------------------------#
# PRIVATE METHODS
#----------------------------------------------------------------------------#

def _isPythonPackage(dirPath):
    if dirPath == '.':
        return True

    dirPath = dirPath.lstrip('./').split('/')

    checkedPath = dirPath[0]
    if not os.path.exists(os.path.join(checkedPath, '__init__.py')):
        return False

    while dirPath:
        checkedPath = os.path.join(checkedPath, dirPath.pop(0))
        if not os.path.exists(os.path.join(checkedPath, '__init__.py')):
            return False
    else:
        return True

#----------------------------------------------------------------------------#

def _pythonWalk(basePath, excludes=[]):
    """
    Similar to os.walk(), but only enters subdirectories which are python
    packages.
    """
    excludes = map(os.path.abspath, excludes)

    dirStack = [basePath]

    while dirStack:
        currentDir = dirStack.pop()

        files = []
        for filename in os.listdir(currentDir):
            # We have some files which are excluded from examination.
            if os.path.abspath(filename) in excludes:
                continue

            qualifiedName = os.path.join(currentDir, filename)
            if os.path.isdir(qualifiedName):
                # Only recurse into python modules.
                if os.path.exists(os.path.join(qualifiedName, '__init__.py')):
                    dirStack.append(qualifiedName)

            else:
                # Regular file.
                files.append(filename)

        yield (currentDir, files)

    return

#----------------------------------------------------------------------------#
# MODULE EPILOGUE
#----------------------------------------------------------------------------#

def _createOptionParser():
    """Creates an option parser instance to handle command-line options."""
    usage = \
"""%prog [options]

Finds all test suites located in files prefixed like testBlah.py, and merges
runs all tests within them."""

    parser = optparse.OptionParser(usage)

    parser.add_option('--debug', action='store_true', dest='debug',
            default=False, help='Enables debugging mode [False]')

    parser.add_option('-d', '--dirname', action='store', dest='dirname',
            default='.', help="The directory tree to test [.]")

    parser.add_option('--verbosity', '-v', action='store', type='int',
            dest='verbosity', default=1, help="How much detail to show [1]")

    return parser

#----------------------------------------------------------------------------#

def main(argv):
    """ The main method for this module.
    """
    parser = _createOptionParser()
    (options, args) = parser.parse_args(argv)

    if args:
        parser.print_help()
        sys.exit(1)

    if not options.debug:
        # we don't want psyco in debugging mode, since it merges together
        # stack frames
        try:
            import psyco
            psyco.profile()
        except:
            pass

    completeSuite = dynamicSuite(options.dirname)
    unittest.TextTestRunner(verbosity=options.verbosity).run(completeSuite)
    
    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

#----------------------------------------------------------------------------#
  
# vim: ts=4 sw=4 sts=4 et tw=78:
