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


class TatoebaLinksReader(TatoebaDictMixin, TatoebaReader):
    def __init__(self, links, sentence_ids=None, sentence_ids_filter='both'):
        """
        A class which reads a Tatoeba links.csv file.

        :param links:
            A file path or file-like object pointing to the links.csv file.

        :param sentence_ids:
            If passed, this restricts which links will be read in to those where
            both the sentence and its translation are on the list of sentence
            IDs. By default, no restriction is imposed.

        :param sentence_ids_filter:
            A string representing how sentence ids are filtered. The options
            are:
                * ``'sent_id'``: Filter only on the sentence id.
                * ``'trans_id'``: Filter only on the translation id.
                * ``'both'``: Filter on both sentence id and translation id.
        """
        self._sentence_ids_filter_str = None
        self._sentence_id_subset(sentence_ids)
        self._sentence_ids_filter(sentence_ids_filter)
        self.links = links

    def group(self, sent_id):
        """
        Retrieve the group of linked sentences that a given sentence belongs to.

        :param sent_id:
            A valid sentence ID.

        :raises InvalidIDError:
            Raised if the sentence is not in any of the linked groups

        :return:
            Returns a :py:class:`frozenset` of sentence IDs which form a
            translation group.
        """

        try:
            return self[sent_id]
        except KeyError as e:
            raise_from(InvalidIDError('Could not find sentence ID '
                                      '{} in any groups'.format(sent_id)), e)

    def groups(self):
        """
        Retrieves a list of all translation groups.

        :return:
            Returns a :py:class:`list` of :py:class:`frozenset` instances
            containing sentence IDs which form a translation group.
        """
        return list(self._group_dict.values())

    @property
    def links(self):
        return self._links_src

    @links.setter
    def links(self, src):
        self._links_src = self._get_src_repr(src)

        link_dict = {}
        group_dict = {}

        nodes = 0
        for row in self.load_file(src):
            try:
                sent_id, trans_id = map(int, row)
            except ValueError as e:
                raise_from(InvalidFileError('Invalid links file - '
                                            'files must have 2 columns'), e)
            
            # Check if both endpoints are in the sentence_id_subset
            if ((self._filter_sent and
                 sent_id not in self.sentence_id_subset) or
                (self._filter_trans and
                 trans_id not in self.sentence_id_subset)): 
                continue

            # If the sentence ID is a translation of something we've already
            # seen before, get the existing node location. Otherwise, add a new
            # node
            if sent_id in link_dict:
                node_id = link_dict[sent_id]
                new_ids = {trans_id}
            elif trans_id in link_dict:
                node_id = link_dict[trans_id]
                new_ids = {sent_id}
            else:
                node_id = nodes
                nodes += 1
                new_ids = {trans_id, sent_id}

            group_dict.setdefault(node_id, set())
            group_dict[node_id] |= new_ids
            link_dict.update({k: node_id for k in new_ids})

        self._link_dict = link_dict
        self._group_dict = {k: frozenset(v) for k, v in iteritems(group_dict)}

    @property
    def sentence_ids_filter(self):
        return self._sentence_ids_filter_str

    def _sentence_ids_filter(self, valstr):
        filter_values = {'sent_id': (True, False),
                         'trans_id': (False, True),
                         'both': (True, True)}

        valstr = valstr.lower()
        if valstr not in filter_values:
            raise ValueError('Invalid sentence_ids_filter: {}'.format(valstr))

        if self.sentence_id_subset is None:
            vals = (False, False)
        else:
            vals = filter_values[valstr]

        self._filter_sent, self._filter_trans = vals
        self._sentence_ids_filter_str = valstr

    @property
    def sentence_id_subset(self):
        return self._sentence_id_subset

    def _sentence_id_subset(self, value):
        self._sentence_id_subset = set(value) if value is not None else None

    @property
    def _base_dict(self):
        return self._link_dict
    
    def __getitem__(self, key):
        return self._group_dict[self._link_dict[key]]

    def __repr__(self):
        return "{}(links='{}')".format(self.__class__.__name__, self.links)


class MissingDataError(ValueError):
    pass

class InvalidFileError(ValueError):
    pass

class InvalidIDError(KeyError):
    pass

