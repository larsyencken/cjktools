# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# dictionaryFormat.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Fri Dec 22 15:18:13 2006
#
#----------------------------------------------------------------------------#

"""
An abstract dictionary interface. Quickly provides an interface to any
dictionary which is line-based, and whose entries are flat text, and thus
amenable to being parsed with regular expressions. The list of known
formats is provided in the knownFormats object. 
"""

#----------------------------------------------------------------------------#

import re
import os, sys

from cjktools.common import sopen
from cjktools.exceptions import NotYetImplementedError
from bilingualDict import BilingualDictionary, DictionaryEntry
import languages

#----------------------------------------------------------------------------#

class UnknownFormatError(Exception):
    """
    Indicates that the dictionary which we attempted to parse had an
    unknown format.
    """
    pass

#----------------------------------------------------------------------------#

class FormatError(Exception):
    """
    Used when a dictionary's data is malformed.
    """
    pass

#----------------------------------------------------------------------------#

class DuplicateEntryError(Exception):
    """
    Used when a dictionary entry has been duplicated. We can safely skip
    it.
    """
    pass

#----------------------------------------------------------------------------#

class DictionaryFormat(object):
    """
    An abstract dictionary format, providing the elements.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def matchHeader(self, headerLine):
        """
        Returns True if the header pattern matches the line given,
        False otherwise.
        """
        raise NotYetImplementedError

    #------------------------------------------------------------------------#

    def parseLine(self, entryLine):
        """
        Parses a dictionary entry from the given line.
        """
        raise NotYetImplementedError

    #------------------------------------------------------------------------#

    def parseDictionary(self, filename):
        """
        Parses the given filename using this format, returning a
        dictionary object containing all the dictionary entries.
        """
        # Determine the source and target language.
        sourceLang, targetLang = detectLanguage(filename)

        iStream = sopen(filename, 'r')
        header = iStream.readline()

        if not self.matchHeader(header):
            raise UnknownFormatError, filename

        dictObj = BilingualDictionary(self, sourceLang, targetLang)
        for line in iStream:
            entry = self.parseLine(line)

            if entry.word in dictObj:
                # Already an entry here, so update it with new readings and
                # senses.
                oldEntry = dictObj[entry.word]
                oldEntry.update(entry)
            else:
                dictObj[entry.word] = entry

        iStream.close()

        return dictObj

    #------------------------------------------------------------------------#

    def iterEntries(self, filename):
        """
        Parses the given filename using this format, returning a
        dictionary object containing all the dictionary entries.
        """
        # Determine the source and target language.
        sourceLang, targetLang = detectLanguage(filename)

        iStream = sopen(filename, 'r')
        header = iStream.readline()

        if not self.matchHeader(header):
            raise UnknownFormatError, filename

        dictObj = BilingualDictionary(self, sourceLang, targetLang)
        for line in iStream:
            yield self.parseLine(line)

        iStream.close()

        return

    #------------------------------------------------------------------------#
    # PRIVATE
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

class RegexFormat(DictionaryFormat):
    """
    Describes a dictionary format, by providing regular expressions
    for the header, the entry lines, and senses within an entry line. The
    entry line pattern should have named values called 'word', 'reading',
    and 'senses'.
    """

    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, name, headerPattern, linePattern, sensePattern):
        """
        Constructor.
        """
        self.name = name
        self.headerPattern = re.compile(headerPattern, re.UNICODE)
        self.linePattern = re.compile(linePattern, re.UNICODE)
        self.sensePattern = re.compile(sensePattern, re.UNICODE)
        return

    #------------------------------------------------------------------------#

    def matchHeader(self, headerLine):
        """
        See parent class.
        """
        return bool(self.headerPattern.match(headerLine))

    #------------------------------------------------------------------------#

    def parseLine(self, entryLine):
        """
        See parent class.
        """
        match = self.linePattern.match(entryLine)
        if not match:
            raise FormatError, u"Bad line: %s" % entryLine
        
        matchDict = match.groupdict()

        word = matchDict['word'].replace(' ', '')
        reading = (matchDict.get('reading') or word).replace(' ', '')
        readings = [reading]
        senseLine = matchDict.get('senses')

        senses = []
        for match in self.sensePattern.finditer(senseLine):
            senses.append(match.groupdict()['sense'])

        if not senses:
            raise FormatError, u"No senses for word: %s" % word

        return DictionaryEntry(word, readings, senses)

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

def detectLanguage(filename):
    """
    Tries to determine the source and target language of a given
    dictionary from its filename. Defaults to 'Unknown', 'Unknown' if the
    correct langauge cannot be worked out.
    """
    filename = os.path.basename(filename)
    if len(filename) > 3 and filename[2] == '_':
        fromCode = filename[0]
        toCode = filename[1]

        try:
            fromLang = languages.fromOneCharCode[fromCode]
            toLang = languages.fromOneCharCode[toCode]
            return fromLang, toLang
        except KeyError:
            pass

    return 'Unknown', 'Unknown'

#----------------------------------------------------------------------------#

