# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# bilingualDict.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 26 13:57:31 2006
#
#----------------------------------------------------------------------------#

"""
A generic bilingual dictionary class.
"""

#----------------------------------------------------------------------------#

from cjktools.enum import Enum
from cjktools.exceptions import NotYetImplementedError

#----------------------------------------------------------------------------#

ClashPolicy = Enum('Overwrite', 'Merge')

#----------------------------------------------------------------------------#

class BilingualDictionary(dict):
    """
    An abstract bilingual dictionary, containing headwords in one
    language and translated senses in another language. Homographs are
    stored as senses of the same lexeme, rather than being separate.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, format, sourceLanguage, targetLanguage):
        """
        Constructor.

        @param format: The format object for this dictionary.
        @type format: DictionaryFormat
        @param sourceLangauge: The source language used for headwords.
        @type sourceLangauge: str
        @param targetLanguage: The target language used for the translated
            meanings.
        @type targetLanguage: str
        """
        self.format = format
        self.sourceLanguage = sourceLanguage
        self.targetLanguage = targetLanguage
        return

    #------------------------------------------------------------------------#

    def update(self, rhsDictionary, clashPolicy=ClashPolicy.Overwrite):
        """
        Merges another dictionary into this one, in-place. Entries are
        """
        if self.sourceLanguage != rhsDictionary.sourceLanguage or \
                self.targetLanguage != rhsDictionary.targetLanguage:
            raise Exception, "Source and target languages must be identical"

        if clashPolicy == ClashPolicy.Merge:
            raise NotYetImplementedError

        return dict.update(self, rhsDictionary)

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

class DictionaryEntry(object):
    """
    A single entry in a dictionary, representing a word, it's reading,
    and its translation into senses.
    """
    __slots__ = ('word', 'readings', 'senses')

    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, word, readings, senses):
        """
        Constructor. There should be either one reading, or one per sense.
        """
        assert len(readings) == 1 or len(readings) == len(senses)
        self.word = word
        self.readings = readings
        self.senses = senses
        return

    #------------------------------------------------------------------------#

    def update(self, rhsEntry):
        """
        Update this entry with readings and senses from another homograph.
        The additional readings and senses are added to this entry.
        
        @param rhsEntry: Another entry to update details from.
        @type rhsEntry: DictionaryEntry
        """
        if not self.word == rhsEntry.word:
            raise Exception, "Can only merge homographs"

        #print 'Merging entries for %s' % self.word
        # If we have only one reading, pad to the number of senses so that
        # we have one sense per reading.
        if len(self.readings) == 1:
            self.readings = len(self.senses)*self.readings

        # Do the same for the rhsEntry.
        if len(rhsEntry.readings) == 1:
            rhsEntry.readings = len(rhsEntry.senses)*rhsEntry.readings

        # Add the readings and senses from the other entry.
        self.readings += rhsEntry.readings
        self.senses += rhsEntry.senses

        return

    #------------------------------------------------------------------------#

    def sensesByReading(self):
        """Returns a dictionary mapping reading to senses."""
        result = {}
        if len(self.readings) > 1:
            assert len(self.senses) == len(self.readings)
            for reading, sense in zip(self.readings, self.senses):
                senseList = result.setdefault(reading, [])
                senseList.append(sense)
        else:
            uniqueReading, = self.readings
            result[uniqueReading] = self.senses[:]

        return result

    #------------------------------------------------------------------------#

    def __repr__(self):
        return unicode(self)

    #------------------------------------------------------------------------#

    def __unicode__(self):
        return u'<DictionaryEntry: %s (%s readings, %s senses)>' % (
                self.word,
                len(set(self.readings)),
                len(self.senses),
            )

    #------------------------------------------------------------------------#

    def __hash__(self):
        return hash(self.name, tuple(self.readings), tuple(self.senses))

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

