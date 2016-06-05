# -*- coding: utf-8 -*-
#
#  test_tatoeba.py
#  cjktools
#

from __future__ import unicode_literals

import os
from io import StringIO
import unittest

from datetime import datetime

from cjktools.resources import tatoeba
from cjktools.common import sopen

def get_data_locs(suffix='_00', extension='.csv'):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_loc = os.path.join(script_dir, 'sample_data/')
    base_names = dict(sentences='sentences',
                      jpn_indices='jpn_indices',
                      links='links',
                      sentences_detailed='sentences_detailed')

    return {k: os.path.join(data_loc, v + suffix + extension)
               for k, v in base_names.items()}

base_data_locs = get_data_locs()


class TatoebaReaderTest(unittest.TestCase):
    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            tatoeba.TatoebaReader()


class TatoebaSentenceReaderTest(unittest.TestCase):
    _resource_name = 'sentences'

    def data_locs(self):
        return base_data_locs

    def sentences_fpath(self):
        return self.data_locs()[self._resource_name]

    def load_file(self, **kwargs):
        """
        Loads the file into a TatoebaSentenceReader object.
        """
        resource_fpath = self.sentences_fpath()

        sreader = tatoeba.TatoebaSentenceReader(
            sentences=resource_fpath,
            **kwargs)

        return sreader

    def test_basic(self):
        # Test that all the sentence IDs load properly
        sr = self.load_file()

        sent_ids = [
            29390, 36809, 46235, 54432, 62093, 68807, 82526, 93620, 109744,
            112733, 156245, 192227, 199398, 208975, 224758, 231440, 258289,
            290943, 293946, 310087, 321190, 410787, 2031040, 2031042
        ]

        self.assertEqual(sorted(sr.keys()), sent_ids)
        self.assertEqual(sorted(sr.keys()), sorted(sr.sentence_ids))

    def test_language_filter(self):
        sr = self.load_file(languages={'fra', 'pol', 'rus'})

        sent_ids = [6381, 508870, 2172488]

        self.assertEqual(sorted(sr.keys()), sent_ids)

    def test_custom_filter_row(self):
        class TatoebaSentenceSubsetReader(tatoeba.TatoebaSentenceReader):
            def __init__(self, sentences, subset=None, **kwargs):
                self._subset = set(subset)

                super(TatoebaSentenceSubsetReader, self).__init__(
                    sentences, **kwargs)

            def filter_row(self, row):
                return int(row[0]) not in self._subset

        sr = TatoebaSentenceSubsetReader(
            sentences=self.sentences_fpath(),
            subset={224758, 6381, 29390},
            languages={'eng', 'jpn'})

        sent_inds = [29390, 224758]

        self.assertEqual(sorted(sr.keys()), sent_inds)

    def test_language(self):
        sr = self.load_file()

        for sent_id in [82526, 93620, 109744, 208975]:
            self.assertEqual(sr.language(sent_id), 'jpn')

        for sent_id in [36809, 293946, 410787, 2031042]:
            self.assertEqual(sr.language(sent_id), 'eng')

    def test_language_error(self):
        sr = self.load_file()

        with self.assertRaises(tatoeba.InvalidIDError):
            sr.language(193)

    def test_sentence(self):
        sr = self.load_file()

        sentence_pairs = [
            (192227, 'ロールプレイングのテレビゲームは時間を食う。'),
            (29390, 'Role-playing video games are time consuming.'),
            (208975, 'その上手な運転手は車の列を縫うように車を走らせた。'),
            (46235, 'The good driver wove his way through the traffic.')
        ]

        for sent_id, sentence in sentence_pairs:
            self.assertEqual(sr[sent_id], sentence)

    def test_sentence_error(self):
        sr = self.load_file()

        with self.assertRaises(tatoeba.InvalidIDError):
            sr.sentence(24)

    def test_details_error(self):
        sr = self.load_file()

        # One that is in the data set
        with self.assertRaises(tatoeba.MissingDataError):
            sr.details(192227)

        # One that's not in the data set
        with self.assertRaises(tatoeba.MissingDataError):
            sr.details(0)

    def test_repr(self):
        sr = self.load_file()

        expected_fmt = "TatoebaSentenceReader(sentences='{}')"
        expected = expected_fmt.format(self.sentences_fpath())

        self.assertEqual(repr(sr), expected)


class TatoebaSentenceReaderDetailedTest(TatoebaSentenceReaderTest):
    _resource_name = 'sentences_detailed'

    def test_details(self):
        sr = self.load_file()

        # Note: I modified 410787 in the csv to make the added/modified
        # different.
        details_pairs = [
            (82526, (None, None, None)),
            (199398, (None, None, None)),
            (258289, ('CK', None, datetime(2010, 10, 7, 15, 55, 17))),
            (410787, ('CK',
                      datetime(2010, 6, 24, 14, 20, 10),
                      datetime(2010, 6, 24, 14, 20, 28)))
        ]

        for sent_id, details in details_pairs:
            self.assertEqual(sr.details(sent_id), details)

    def test_details_error(self):
        sr = self.load_file()

        with self.assertRaises(tatoeba.InvalidIDError):
            sr.details(24)


class TatoebaSentenceReaderMiscTests(unittest.TestCase):
    def test_invalid_file(self):
        # Too few columns
        invalid_1 = StringIO('3444\teng\n3949\tjp\n')
        with self.assertRaises(tatoeba.InvalidFileError):
            sr = tatoeba.TatoebaSentenceReader(invalid_1)

        # Too many for undetailed, too few for detailed
        invalid_2 = StringIO('3444\teng\tThe boy ate a tiger\tMB')
        with self.assertRaises(tatoeba.InvalidFileError):
            sr = tatoeba.TatoebaSentenceReader(invalid_2)

        # Too many even for detailed
        invalid_3 = StringIO('3444\teng\tThe boy ate a tiger\tMB\t\\N\t\\N\t\\N')
        with self.assertRaises(tatoeba.InvalidFileError):
            sr = tatoeba.TatoebaSentenceReader(invalid_3)


class FileObjReaderMixin(object):
    """
    Mixin to run the existing tests using an already opened file object.
    """
    def load_file(self, **kwargs):
        with open(self.sentences_fpath(), mode='r') as sentences_file:
            sentences_file.filename = self.sentences_fpath()
            sreader = tatoeba.TatoebaSentenceReader(
                sentences=sentences_file,
                **kwargs)

        return sreader

class TatoebaSentenceReaderFObjTest(FileObjReaderMixin,
                                    TatoebaSentenceReaderTest):
    pass

class TatoebaSentenceReaderDetailedFObjTest(FileObjReaderMixin,
                                            TatoebaSentenceReaderDetailedTest):
    pass



    
