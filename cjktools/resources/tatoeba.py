# -*- coding: utf-8 -*-
#
#  tatoeba.py
#  cjktools
#

import csv
import itertools

from datetime import datetime
from collections import defaultdict, Mapping

from six import raise_from, iteritems

from cjktools.common import sopen, _NullContextWrapper

class TatoebaReader(object):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('This is an abstract base class '
                                  'and should not be instantiated')

    def load_file(self, fpath_or_buf, **csv_kwargs):
        """
        A generator reading a given file line by line.

        :param fpath_or_buf:
            This can either be a file path or open file buffer.

        :param csv_kwargs:
            By default, the kwargs passed to :py:func:`csv.reader` are those for
            a standard Tatoeba file. You can pass additional keyword arguments
            here.
        """
        reader_kwargs = dict(delimiter='\t')
        reader_kwargs.update(csv_kwargs)

        if getattr(fpath_or_buf, 'read', None) is None:
            cfile = sopen(fpath_or_buf, mode='r')
        else:
            cfile = _NullContextWrapper(fpath_or_buf)

        with cfile as f:
            reader = csv.reader(f, **reader_kwargs)

            for row in reader:
                yield row

    def _get_src_repr(self, src):
        """ Get the string representation of the source (filename or repr) """
        if getattr(src, 'read', None) is None:
            return src
        else:
            return getattr(src, 'filename', repr(src))


class TatoebaDictMixin(Mapping):
    def __getitem__(self, key):
        return self._base_dict.__getitem__(key)

    def __iter__(self):
        return self._base_dict.__iter__()

    def __len__(self):
        return self._base_dict.__len__()


class TatoebaSentenceReader(TatoebaDictMixin, TatoebaReader):
    def __init__(self, sentences, languages={'jpn', 'eng'}):
        self.languages = languages
        self.sentences = sentences

    def language(self, sent_id):
        """
        Retrieve the language of a given sentence.

        :param sent_id:
            A valid sentence id.

        :raises InvalidIDError:
            Raised if an invalid ID is passed.
        """
        for lang, sent_id_set in iteritems(self._language_dict):
            if sent_id in sent_id_set:
                return lang

        raise InvalidIDError('No language found '
                             'for sentence id {}'.format(sent_id))

    def sentence(self, sent_id):
        """
        Retrieve a sentence given a sentence ID.

        :param sent_id:
            A valid sentence id.

        :raises InvalidIDError:
            Raised if an invalid ID is passed.
        """
        try:
            return self[sent_id]
        except KeyError as e:
            raise_from(InvalidIDError('Could not find sentence '
                                      'with ID {}'.format(sent_id)), e)

    def details(self, sent_id):
        """
        Retrieve additional details about a given sentence.

        :param sent_id:
            A valid sentence ID.

        :raises MissingDataError:
            Raised if detailed sentence information was not loaded into the
            reader.

        :raises InvalidIDError:
            Raised if an invalid sentence ID is passed.

        :returns:
            Returns a tuple of the form:

            ``(username, date_added, date_modified)``

            All three are strings. 
        """
        if self._detailed_info_dict is None:
            raise MissingDataError('Detailed information not loaded.')

        try:
            return self._detailed_info_dict[sent_id]
        except KeyError as e:
            raise_from(InvalidIDError('Detailed information not found for '
                                      'sentence ID {}'.format(sent_id)), e)

    @property
    def sentences(self):
        """
        The source of the sentences that have been read.
        """
        return self._sentences_src

    @sentences.setter
    def sentences(self, src):
        self._sentences_src = self._get_src_repr(src)

        sentence_gen = self.load_file(src)

        # Infer if this is sentences or sentences_detailed
        first_row = next(sentence_gen)
        if len(first_row) == 3:
            sentences_detailed = False
        elif len(first_row) == 6:
            sentences_detailed = True
        else:
            raise InvalidFileError('Invalid sentences file, files'
                                   'must have either 3 or 6 columns.')

        # Prepare output dictionaries
        language_dict = defaultdict(set)
        sentence_dict = {}

        if sentences_detailed:
            detailed_info_dict = {}
        else:
            detailed_info_dict = None

        # Read in all rows
        for row in itertools.chain([first_row], sentence_gen):
            if self.filter_row(row):
                continue

            sent_id, lang, text = row[0:3]

            if self.languages is not None and lang not in self.languages:
                continue

            sent_id = int(sent_id)

            language_dict[lang].add(sent_id)
            sentence_dict[sent_id] = text

            if sentences_detailed:
                uname, d_added, d_modified = row[3:6]

                uname = None if uname == r'\N' else uname
                d_added, d_modified = map(self.parse_date,
                                          (d_added, d_modified))

                detailed_info_dict[sent_id] = (uname, d_added, d_modified)

        # Assign the read dictionaries
        self._language_dict = dict(language_dict)
        self._sentence_dict = sentence_dict
        self._detailed_info_dict = detailed_info_dict

    @property
    def sentence_ids(self):
        """
        All the sentence ids that have been loaded into the reader.
        """
        return self._sentence_dict.keys()

    @property
    def _base_dict(self):
        return self._sentence_dict

    datetime_format = '%Y-%m-%d %H:%M:%S'
    def parse_date(self, dtstr):
        """
        Parser for dates in detailed information.
        """
        if dtstr == r'\N':
            return None

        return datetime.strptime(dtstr, self.datetime_format)

    def filter_row(self, row):
        return False

    def __repr__(self):
        return "{}(sentences='{}')".format(self.__class__.__name__,
                                           self.sentences)


class MissingDataError(ValueError):
    pass

class InvalidFileError(ValueError):
    pass

class InvalidIDError(KeyError):
    pass

