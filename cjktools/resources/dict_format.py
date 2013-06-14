# -*- coding: utf-8 -*-
#
#  dict_format.py
#  cjktools
#

"""
An abstract dictionary interface. Quickly provides an interface to any
dictionary which is line-based, and whose entries are flat text, and thus
amenable to being parsed with regular expressions. The list of known
formats is provided in the known_formats object.
"""

import re

from cjktools.errors import NotYetImplementedError
from bilingual_dict import BilingualDictionary, DictionaryEntry


class UnknownFormatError(Exception):
    """
    Indicates that the dictionary which we attempted to parse had an
    unknown format.
    """
    pass


class FormatError(Exception):
    "Used when a dictionary's data is malformed."
    pass


class DuplicateEntryError(Exception):
    "Used when a dictionary entry has been duplicated. We can safely skip it."
    pass


class DictionaryFormat(object):
    "An abstract dictionary format, providing the elements."
    def match_header(self, header_line):
        """
        Returns True if the header pattern matches the line given,
        False otherwise.
        """
        raise NotYetImplementedError

    def parse_line(self, entry_line):
        "Parses a dictionary entry from the given line."
        raise NotYetImplementedError

    def parse_dictionary(self, lines):
        """
        Parses the given filename using this format, returning a
        dictionary object containing all the dictionary entries.
        """
        b = BilingualDictionary(self)
        for line in lines:
            entry = self.parse_line(line)

            if entry.word in b:
                b[entry.word].update(entry)
            else:
                b[entry.word] = entry

        return b

    def iter_entries(self, lines):
        """
        Parses the given filename using this format, returning a
        dictionary object containing all the dictionary entries.
        """
        for line in lines:
            yield self.parse_line(line)


class RegexFormat(DictionaryFormat):
    """
    Describes a dictionary format, by providing regular expressions
    for the header, the entry lines, and senses within an entry line. The
    entry line pattern should have named values called 'word', 'reading',
    and 'senses'.
    """

    def __init__(self, name, header_pattern, line_pattern, sense_pattern):
        self.name = name
        self.header_pattern = re.compile(header_pattern, re.UNICODE)
        self.line_pattern = re.compile(line_pattern, re.UNICODE)
        self.sense_pattern = re.compile(sense_pattern, re.UNICODE)

    def match_header(self, header_line):
        return bool(self.header_pattern.match(header_line))

    def parse_line(self, entry_line):
        match = self.line_pattern.match(entry_line)
        if not match:
            raise FormatError(u"Bad line: %s" % entry_line)

        match_dict = match.groupdict()

        word = match_dict['word'].replace(' ', '')
        reading = (match_dict.get('reading') or word).replace(' ', '')
        readings = [reading]
        sense_line = match_dict.get('senses')

        senses = []
        for match in self.sense_pattern.finditer(sense_line):
            senses.append(match.groupdict()['sense'])

        if not senses:
            raise FormatError(u"No senses for word: %s" % word)

        return DictionaryEntry(word, readings, senses)
