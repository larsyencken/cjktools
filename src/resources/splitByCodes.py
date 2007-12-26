#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# splitByCodes.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Jun 13 10:10:23 EST 2007
#
#----------------------------------------------------------------------------#

import os, sys, optparse
import re
from cjktools.common import sopen

from autoFormat import iterEntries

#----------------------------------------------------------------------------#
# PUBLIC
#----------------------------------------------------------------------------#

def loadCodedDictionary(filename):
    """
    Load a dictionary which is split by the codes within it.
    """
    wordToEntry = {} 
    codedDict = {}
    for entry in iterEntries(filename):
        word = entry.word

        # Merge any word entries with the same graphical form.
        if word in wordToEntry:
            firstEntry = wordToEntry[word]
            firstEntry.update(entry)
            entry = firstEntry
        else:
            wordToEntry[word] = entry

        codes = getCodes('/'.join(entry.senses))

        # Create a subset of the dictionary for each code.
        for code in codes:
            subDict = codedDict.setdefault(code, {})

            # Note that overwriting is ok, since we already merged any
            # coincidental forms.
            subDict[word] = entry

    return codedDict

#----------------------------------------------------------------------------#

def iterCodedEntries(filename):
    """
    Returns an iterator over dictionary entries in the filename, with their
    parsed codes, in (entry, codeList) pairs.
    """
    for entry in iterEntries(filename):
        codes = getCodes('/'.join(entry.senses))
        yield entry, codes

    return

#----------------------------------------------------------------------------#

_codePattern = re.compile(u'\(([a-z,]+)\)', re.UNICODE)

def getCodes(line, filterSet=[]):
    """
    Returns the dictionary codes found in the given line. 
    """
    matches = _codePattern.findall(line)
    codes = []
    for match in matches:
        if ' ' not in match:
            codes.extend([c for c in match.split(',') if c not in filterSet])

    return codes
 
#----------------------------------------------------------------------------#

_englishWords = '/usr/share/dict/words'

def splitByCodes(inputFile, outputFile, ignores=[]):
    """
    Splits the dictionary into separate files based on the codes present.
    """
    iStream = sopen(inputFile, 'r')
    oStream = sopen(outputFile, 'w')

    knownWords = set([l.rstrip().lower() for l in open(_englishWords)])
    knownWords = set([w for w in knownWords if len(w) > 3])

    codeStreams = {}

    lines = iter(iStream)
    header = iStream.next()

    for line in iStream:
        codes = getCodes(line, knownWords)

        for code in codes:
            oStream = codeStreams.get(code)
            if oStream is None:
                print 'Found new code: %s' % code
                oStream = codeStreams.setdefault(
                        code, 
                        sopen('%s.%s' % (outputFile, code), 'w')
                    )
                oStream.write(header)
            oStream.write(line)

    iStream.close()

    for oStream in codeStreams.values():
        oStream.close()

    return

#----------------------------------------------------------------------------#
# PRIVATE
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# MODULE EPILOGUE
#----------------------------------------------------------------------------#

def _createOptionParser():
    """
    Creates an option parser instance to handle command-line options.
    """
    usage = \
"""%prog [options] inputFile outputFile

Splits an edict format dictionary into multiple files by the codes used."""

    parser = optparse.OptionParser(usage)

    parser.add_option('--debug', action='store_true', dest='debug',
            default=False, help='Enables debugging mode [False]')

    parser.add_option('--ignore', '-i', action='store', dest='ignore',
            default='', help='A comma separated list of tags to ignore.')

    return parser

#----------------------------------------------------------------------------#

def main(argv):
    """
    The main method for this module.
    """
    parser = _createOptionParser()
    (options, args) = parser.parse_args(argv)

    try:
        [inputFile, outputFile] = args
    except:
        parser.print_help()
        sys.exit(1)

    # Avoid psyco in debugging mode, since it merges stack frames.
    if not options.debug:
        try:
            import psyco
            psyco.profile()
        except:
            pass

    splitByCodes(inputFile, outputFile, ignores=options.ignore.split(','))
    
    return

#----------------------------------------------------------------------------#

if __name__ == '__main__':
    main(sys.argv[1:])

#----------------------------------------------------------------------------#
  
# vim: ts=4 sw=4 sts=4 et tw=78:

