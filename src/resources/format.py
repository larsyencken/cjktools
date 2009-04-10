# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# dictionary_format.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Fri Dec 22 15:18:13 2006
#
#----------------------------------------------------------------------------#

"""
An abstract dictionary interface. Quickly provides an interface to any
dictionary which is line-based, and whose entries are flat text, and thus
amenable to being parsed with regular expressions. The list of known
formats is provided in the known_formats object. 
"""

#----------------------------------------------------------------------------#

import re
import os, sys

from cjktools.common import sopen
from cjktools.exceptions import NotYetImplementedError
from bilingual_dict import BilingualDictionary, DictionaryEntry
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

    def match_header(self, header_line):
        """
        Returns True if the header pattern matches the line given,
        False otherwise.
        """
        raise NotYetImplementedError

    #------------------------------------------------------------------------#

    def parse_line(self, entry_line):
        """
        Parses a dictionary entry from the given line.
        """
        raise NotYetImplementedError

    #------------------------------------------------------------------------#

    def parse_dictionary(self, filename):
        """
        Parses the given filename using this format, returning a
        dictionary object containing all the dictionary entries.
        """
        # Determine the source and target language.
        source_lang, target_lang = detect_language(filename)

        i_stream = sopen(filename, 'r')
        header = i_stream.readline()

        if not self.match_header(header):
            raise UnknownFormatError, filename

        dict_obj = BilingualDictionary(self, source_lang, target_lang)
        for line in i_stream:
            entry = self.parse_line(line)

            if entry.word in dict_obj:
                # Already an entry here, so update it with new readings and
                # senses.
                old_entry = dict_obj[entry.word]
                old_entry.update(entry)
            else:
                dict_obj[entry.word] = entry

        i_stream.close()

        return dict_obj

    #------------------------------------------------------------------------#

    def iter_entries(self, filename):
        """
        Parses the given filename using this format, returning a
        dictionary object containing all the dictionary entries.
        """
        # Determine the source and target language.
        source_lang, target_lang = detect_language(filename)

        i_stream = sopen(filename, 'r')
        header = i_stream.readline()

        if not self.match_header(header):
            raise UnknownFormatError, filename

        dict_obj = BilingualDictionary(self, source_lang, target_lang)
        for line in i_stream:
            yield self.parse_line(line)

        i_stream.close()

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

    def __init__(self, name, header_pattern, line_pattern, sense_pattern):
        """
        Constructor.
        """
        self.name = name
        self.header_pattern = re.compile(header_pattern, re.UNICODE)
        self.line_pattern = re.compile(line_pattern, re.UNICODE)
        self.sense_pattern = re.compile(sense_pattern, re.UNICODE)
        return

    #------------------------------------------------------------------------#

    def match_header(self, header_line):
        """
        See parent class.
        """
        return bool(self.header_pattern.match(header_line))

    #------------------------------------------------------------------------#

    def parse_line(self, entry_line):
        """
        See parent class.
        """
        match = self.line_pattern.match(entry_line)
        if not match:
            raise FormatError, u"Bad line: %s" % entry_line
        
        match_dict = match.groupdict()

        word = match_dict['word'].replace(' ', '')
        reading = (match_dict.get('reading') or word).replace(' ', '')
        readings = [reading]
        sense_line = match_dict.get('senses')

        senses = []
        for match in self.sense_pattern.finditer(sense_line):
            senses.append(match.groupdict()['sense'])

        if not senses:
            raise FormatError, u"No senses for word: %s" % word

        return DictionaryEntry(word, readings, senses)

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

def detect_language(filename):
    """
    Tries to determine the source and target language of a given
    dictionary from its filename. Defaults to 'Unknown', 'Unknown' if the
    correct langauge cannot be worked out.
    """
    filename = os.path.basename(filename)
    if len(filename) > 3 and filename[2] == '_':
        from_code = filename[0]
        to_code = filename[1]

        try:
            from_lang = languages.from_one_char_code[from_code]
            to_lang = languages.from_one_char_code[to_code]
            return from_lang, to_lang
        except KeyError:
            pass

    return 'Unknown', 'Unknown'

#----------------------------------------------------------------------------#

