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

def dynamic_suite(file_or_directory, excludes=[], base_import_path=[]):
    """
    Generates a dynamic test suite out of the given directory.

    If given a filename, it tests only that file. If given a directory name,
    it tests all python packages under that directory.
    """
    original_dir = os.getcwd()
    single_mode = False
    if isdir(file_or_directory):
        root_directory = file_or_directory
    else:
        single_mode = True
        module_filename = file_or_directory
        root_directory = dirname(file_or_directory)

    # Change to the root directory, and ensure we can import from there.
    root_directory = abspath(root_directory)
    os.chdir(root_directory)
    if root_directory not in sys.path:
        sys.path.append(root_directory)

    if single_mode:
        filenames = [module_filename]
        test_filename = 'test' + module_filename[0].upper() + module_filename[1:]
        if exists(test_filename):
            filenames.append(test_filename)
        module_iter = [('.', filenames)]
    else:
        module_iter = _python_walk('.', excludes)

    suites = []

    for dir_path, filenames in module_iter:
        import_path = base_import_path + dir_path.lstrip('.').split('/')[1:]

        for filename in filenames:
            # Import the module.
            module_name = filename[:-len('.py')]
            full_import_path = import_path + [module_name]
            try:
                module = __import__('.'.join(full_import_path))
            except ImportError, e:
                print 'Error importing: %s' % '.'.join(full_import_path)
                print e.message
                print 'Continuing...'
                continue

            # If the one we care about is embedded deep within packages,
            # fetch it out.
            if import_path:
                for sub_module in full_import_path[1:]:
                    module = getattr(module, sub_module)

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
    os.chdir(original_dir)

    return unittest.TestSuite(suites)

#----------------------------------------------------------------------------#
# PRIVATE METHODS
#----------------------------------------------------------------------------#

def _is_python_package(dir_path):
    if dir_path == '.':
        return True

    dir_path = dir_path.lstrip('./').split('/')

    checked_path = dir_path[0]
    if not exists(join(checked_path, '__init__.py')):
        return False

    while dir_path:
        checked_path = join(checked_path, dir_path.pop(0))
        if not exists(join(checked_path, '__init__.py')):
            return False
    else:
        return True

#----------------------------------------------------------------------------#

def _python_walk(base_path, excludes=[]):
    """
    Similar to os.walk(), but only enters subdirectories which are python
    packages.
    """
    excludes = map(abspath, excludes)

    dir_stack = [base_path]

    while dir_stack:
        current_dir = dir_stack.pop()

        files = []
        for filename in os.listdir(current_dir):
            # We have some files which are excluded from examination.
            if abspath(filename) in excludes:
                continue

            qualified_name = join(current_dir, filename)
            if isdir(qualified_name):
                # Only recurse into python modules.
                if exists(join(qualified_name, '__init__.py')):
                    dir_stack.append(qualified_name)

            elif filename.endswith('.py'):
                # Python file.
                files.append(filename)

        yield current_dir, files

    return

#----------------------------------------------------------------------------#
# MODULE EPILOGUE
#----------------------------------------------------------------------------#

def _create_option_parser():
    """Creates an option parser instance to handle command-line options."""
    usage = \
"""%prog [options]

Finds all test suites located in files prefixed like test_blah.py, and merges
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
    parser = _create_option_parser()
    (options, args) = parser.parse_args(argv)

    if args:
        parser.print_help()
        sys.exit(1)

    if options.filename:
        complete_suite = dynamic_suite(options.filename)
    else:
        complete_suite = dynamic_suite(options.dirname)
    unittest.TextTestRunner(verbosity=options.verbosity).run(complete_suite)
    
    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

#----------------------------------------------------------------------------#
  
# vim: ts=4 sw=4 sts=4 et tw=78:
