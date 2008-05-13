#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# dyntest.py
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
import unittest, doctest
from os.path import exists, isdir, join, abspath, dirname

#----------------------------------------------------------------------------#
# PUBLIC METHODS
#----------------------------------------------------------------------------#

def dynamicSuite(fileOrDirectory, excludes=[], baseImportPath=[]):
    """
    Generates a dynamic test suite out of the given directory.

    If given a filename, it tests only that file. If given a directory name,
    it tests all python packages under that directory.
    """
    originalDir = os.getcwd()
    singleMode = False
    if isdir(fileOrDirectory):
        rootDirectory = fileOrDirectory
    else:
        singleMode = True
        moduleFilename = fileOrDirectory
        rootDirectory = dirname(fileOrDirectory)

    # Change to the root directory, and ensure we can import from there.
    rootDirectory = abspath(rootDirectory)
    os.chdir(rootDirectory)
    if rootDirectory not in sys.path:
        sys.path.append(rootDirectory)

    if singleMode:
        filenames = [moduleFilename]
        testFilename = 'test' + moduleFilename[0].upper() + moduleFilename[1:]
        if exists(testFilename):
            filenames.append(testFilename)
        moduleIter = [('.', filenames)]
    else:
        moduleIter = _pythonWalk('.', excludes)

    suites = []

    for dirPath, filenames in moduleIter:
        importPath = baseImportPath + dirPath.lstrip('.').split('/')[1:]

        for filename in filenames:
            # Import the module.
            moduleName = filename[:-len('.py')]
            fullImportPath = importPath + [moduleName]
            try:
                module = __import__('.'.join(fullImportPath))
            except ImportError, e:
                print 'Error importing: %s' % '.'.join(fullImportPath)
                print e.message
                print 'Continuing...'
                continue

            # If the one we care about is embedded deep within packages,
            # fetch it out.
            if importPath:
                for subModule in fullImportPath[1:]:
                    module = getattr(module, subModule)

            if filename.startswith('test'):
                # Test modules have an explicit suite() function by
                # convention.
                suites.append(module.suite())
            else:
                # Code modules can be doctested.
                try:
                    suites.append(doctest.DocTestSuite(module))
                except ValueError:
                    continue
    
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
    if not exists(join(checkedPath, '__init__.py')):
        return False

    while dirPath:
        checkedPath = join(checkedPath, dirPath.pop(0))
        if not exists(join(checkedPath, '__init__.py')):
            return False
    else:
        return True

#----------------------------------------------------------------------------#

def _pythonWalk(basePath, excludes=[]):
    """
    Similar to os.walk(), but only enters subdirectories which are python
    packages.
    """
    excludes = map(abspath, excludes)

    dirStack = [basePath]

    while dirStack:
        currentDir = dirStack.pop()

        files = []
        for filename in os.listdir(currentDir):
            # We have some files which are excluded from examination.
            if abspath(filename) in excludes:
                continue

            qualifiedName = join(currentDir, filename)
            if isdir(qualifiedName):
                # Only recurse into python modules.
                if exists(join(qualifiedName, '__init__.py')):
                    dirStack.append(qualifiedName)

            elif filename.endswith('.py'):
                # Python file.
                files.append(filename)

        yield currentDir, files

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

    parser.add_option('-d', '--dirname', action='store', dest='dirname',
            default='.', help="The directory tree to test [.]")

    parser.add_option('--verbosity', '-v', action='store', type='int',
            dest='verbosity', default=1, help="How much detail to show [1]")

    parser.add_option('-s', '--single', action='store', dest='filename',
            help="Test a single python module.")
            
    return parser

#----------------------------------------------------------------------------#

def main(argv):
    """
    The main method for this module.
    """
    parser = _createOptionParser()
    (options, args) = parser.parse_args(argv)

    if args:
        parser.print_help()
        sys.exit(1)

    if options.filename:
        completeSuite = dynamicSuite(options.filename)
    else:
        completeSuite = dynamicSuite(options.dirname)
    unittest.TextTestRunner(verbosity=options.verbosity).run(completeSuite)
    
    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

#----------------------------------------------------------------------------#
  
# vim: ts=4 sw=4 sts=4 et tw=78:
