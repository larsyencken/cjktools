# -*- coding: utf-8 -*-
#
#  test_tatoeba.py
#  cjktools
#

from __future__ import unicode_literals

import os
from .._common import to_unicode_stream, to_string_stream
import unittest

from six import text_type

from functools import partial
from datetime import datetime

from cjktools.resources import tatoeba, auto_format, cjkdata
from cjktools.common import sopen

from nose_parameterized import parameterized


def get_data_loc(key, suffix='_00', extension='.csv'):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_loc = os.path.join(script_dir, 'sample_data/')
    base_names = dict(sentences='sentences',
                      jpn_indices='jpn_indices',
                      links='links',
                      sentences_detailed='sentences_detailed',
                      edict='je_edict')

    fname = base_names[key] + suffix + extension
    return os.path.join(data_loc, fname)


def get_edict():
    if getattr(get_edict, '_cached', None) is not None:
        return get_edict._cached

    with sopen(get_data_loc('edict', extension=''), mode='r') as edf:
        edict = auto_format.load_dictionary(edf)

    get_edict._cached = edict

    return edict


class ReaderBaseCase(unittest.TestCase):
    def resource_fpath(self):
        return get_data_loc(self._resource_name)

    def load_file(self, resource=None, **kwargs):
        """
        Loads the file into a TatoebaSentenceReader object.
        """
        if resource is None:
            resource = self.resource_fpath()

        reader = self.ReaderClass(resource, **kwargs)
        
        return reader


class FileObjReaderMixin(object):
    """
    Mixin to run the existing tests using an already opened file object.
    """
    def load_file(self, resource=None, **kwargs):
        if resource is None:
            resource = self.resource_fpath()

        with open(self.resource_fpath(), mode='r') as resource_file:
            try:
                resource_file.filename = self.resource_fpath()
            except AttributeError:
                class FileWrapper(object):
                    def __init__(self, fin, fpath):
                        self.f = fin
                        self.filename = fpath

                    def __getattr__(self, attr):
                        return getattr(self.f, attr)

                    def __iter__(self):
                        return iter(self.f)

                resource_file = FileWrapper(resource_file,
                                            self.resource_fpath())

            r = super(FileObjReaderMixin, self).load_file(resource_file,
                                                          **kwargs)

            return r


###
# Tatoeba Reader base class test
class TatoebaReaderTest(unittest.TestCase):
    def test_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            tatoeba.TatoebaReader()


###
# Tatoeba Sentence Reader tests
class TatoebaSentenceReaderTest(ReaderBaseCase):
    _resource_name = 'sentences'
    ReaderClass = tatoeba.TatoebaSentenceReader

    def test_basic(self):
        # Test that all the sentence IDs load properly
        sr = self.load_file()

        sent_ids = [
            6381, 29390, 36809, 46235, 54432, 62093, 68807, 82526, 93620,
            109744, 112733, 156245, 192227, 199398, 208975, 224758, 231440, 258289,
            290943, 293946, 310087, 321190, 410787, 508870, 723598, 817971,
            2031040, 2031042, 2172488
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
            sentences=self.resource_fpath(),
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
        expected = expected_fmt.format(self.resource_fpath())

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
    @parameterized.expand([
        # Too few columns
        ('too_few', '3444\teng\n3949\tjp\n'),
        # Too many for undetailed, too few for detailed
        ('in_between', '3444\teng\tThe boy ate a tiger\tMB'),
        # Too many even for detailed
        ('too_many', '3444\teng\tThe boy ate a tiger\tMB\t\\N\t\\N\t\\N'),
        # In between, but with unicode
        ('in_between_unicode', '3444\teng\tThe boy ate a 虎\tMB')
    ])
    def test_invalid_file(self, name, rowstr):
        invalid = to_string_stream(rowstr)
        with self.assertRaises(tatoeba.InvalidFileError):
            sr = tatoeba.TatoebaSentenceReader(invalid)


class TatoebaSentenceReaderFObjTest(FileObjReaderMixin,
                                    TatoebaSentenceReaderTest):
    pass

class TatoebaSentenceReaderDetailedFObjTest(FileObjReaderMixin,
                                            TatoebaSentenceReaderDetailedTest):
    pass


###
# Tatoeba Links Reader tests

class TatoebaLinksReaderTests(ReaderBaseCase):
    _resource_name = 'links'
    ReaderClass = tatoeba.TatoebaLinksReader

    def test_basic(self):
        lr = self.load_file()

        self.assertEqual(len(lr), 29)

        groups = [
            (6381, {6381, 156245, 258289, 817971}),
            (29390, {29390, 192227}),
            (36809, {36809, 54432, 199398, 410787}),
            (46235, {46235, 208975}),
            (62093, {62093, 224758, 723598, 2031040, 2031042}),
            (68807, {68807, 231440}),
            (82526, {82526, 321190, 508870}),
            (93620, {93620, 310087, 2172488}),
            (109744, {109744, 293946}),
            (112733, {112733, 290943})
        ]

        for sent_id, group in groups:
            self.assertEqual(lr[sent_id], group)
            self.assertEqual(lr.group(sent_id), group)

    def test_filter_both(self):
        subset = {6381, 82526, 258289, 192227, 508870}

        lr = self.load_file(sentence_ids=subset, sentence_ids_filter='both')

        groups = [
            (6381, {6381, 258289}),
            (82526, {82526, 508870})
        ]

        for sent_id, group in groups:
            self.assertEqual(lr[sent_id], group)

        self.assertEqual(lr.sentence_ids_filter, 'both')

    def test_filter_sent_id(self):
        # Normally there isn't much difference between sent_id and
        # trans_id because the links file stores things redundantly, but
        # I've removed all but the 6381->817971 edge in the graph, so it
        # will show up in sent_id, but not in trans_id
        subset = {6381, 82526, 258289, 192227, 508870}
        lr = self.load_file(sentence_ids=subset, sentence_ids_filter='sent_id')

        groups = [
            (6381, {6381, 156245, 258289, 817971}),
            (82526, {82526, 321190, 508870}),
            (29390, {29390, 192227})
        ]

        for sent_id, group in groups:
            self.assertEqual(lr[sent_id], group)

        self.assertEqual(lr.sentence_ids_filter, 'sent_id')

    def test_filter_trans_id(self):
        subset = {6381, 82526, 258289, 192227, 508870}
        lr = self.load_file(sentence_ids=subset, sentence_ids_filter='trans_id')

        groups = [
            (6381, {6381, 156245, 258289}),
            (82526, {82526, 321190, 508870}),
            (29390, {29390, 192227})
        ]

        for sent_id, group in groups:
            self.assertEqual(lr[sent_id], group)

        self.assertEqual(lr.sentence_ids_filter, 'trans_id')

    def test_filter_error(self):
        subset = {6381, 82526, 258289, 192227, 508870}

        with self.assertRaises(ValueError):
            lr = self.load_file(sentence_ids=subset,
                                sentence_ids_filter='banana')

    def test_group_error(self):
        lr = self.load_file()
        with self.assertRaises(tatoeba.InvalidIDError):
            lr.group(100)

    def test_groups(self):
        lr = self.load_file(sentence_ids={6381, 156245, 29390, 192227})

        groups = [
            {6381, 156245},
            {29390, 192227}
        ]

        actual = sorted(lr.groups(), key=lambda x: min(x))

        self.assertEqual(groups, actual)
    
    def test_links(self):
        lr = self.load_file()

        self.assertEqual(lr.links, self.resource_fpath())

    def test_repr(self):
        lr = self.load_file()

        expected_fmt = "TatoebaLinksReader(links='{}')"
        expected = expected_fmt.format(self.resource_fpath())

        self.assertEqual(repr(lr), expected)


class TatoebaLinksReaderMiscTests(unittest.TestCase):
    @parameterized.expand([
        # Too few columns
        ('too_few', '3444\n3949\n'),
        # Too many columns
        ('too_many', '3444\teng\tThe boy ate a tiger\tMB'),
        # Too many columns, with unicode
        ('too_many', '3444\teng\tThe boy ate a tiger (虎)\tMB'),
    ])
    def test_invalid_file(self, name, rowstr):
        # Too few columns
        invalid = to_string_stream(rowstr)
        with self.assertRaises(tatoeba.InvalidFileError):
            sr = tatoeba.TatoebaLinksReader(invalid)

###
# Tanaka word tests
class TanakaWordTests(unittest.TestCase):
    WordClass = tatoeba.TanakaWord
    def _default_args(self, args):
        default_args = (None, None, None, None, False)

        return args + default_args[len(args):]

    @parameterized.expand([
        ('alone', 'は|1', ('は',)),
        ('after_reading', '度(ど)|1', ('度', 'ど')),
        ('before_sense', 'は|1[01]', ('は', None, 1)),
        ('before_disp', 'ばれる|1{ばれた}', ('ばれる', None, None, 'ばれた')),
        ('before_example', 'わっと|2~', ('わっと', None, None, None, True))
    ])
    def test_legacy_tag(self, name, tagstr, expected):
        exp_word = self.WordClass(*self._default_args(expected))

        act = self.WordClass.from_text(tagstr)

        self.assertEqual(exp_word, act)
        self.assertEqual(exp_word.display, act.display)

    @parameterized.expand([
        ('headword', ('を',), 'を'),
        ('reading', ('時', 'とき'), '時(とき)'),
        ('sense', ('が', None, 3), 'が[03]'),
        ('read_sense', ('大学', 'だいがく', 1), '大学(だいがく)[01]'),
        ('display', ('である', None, None, 'であった'), 'である{であった}'),
        ('read_disp', ('為る', 'する', None, 'し'), '為る(する){し}'),
        ('sense_disp', ('其の', None, 1, 'その'), '其の[01]{その}'),
        ('read_sense_disp', ('其の', 'その', 1, 'その'), '其の(その)[01]{その}'),
        ('example', ('ロールプレイング', None, None, None, True),
            'ロールプレイング~'),
        ('read_ex', ('時', 'とき', None, None, True), '時(とき)~'),
        ('sense_ex', ('食う', None, 7, None, True), '食う[07]~'),
        ('read_sense_ex', ('彼', 'かれ', 1, None, True), '彼(かれ)[01]~'),
        ('disp_ex',
            ('ネイティブアメリカン', None, None, 'ネイティブ・アメリカン', True),
            'ネイティブアメリカン{ネイティブ・アメリカン}~'),
        ('read_disp_ex',
            ('喝采を送る', 'かっさいをおくる', None, '喝采を送った', True), 
            '喝采を送る(かっさいをおくる){喝采を送った}~'),
        ('sense_disp_ex', ('ソフト', None, 1, 'ソフトな', True),
            'ソフト[01]{ソフトな}~'),
        ('read_sense_disp_ex', ('立て', 'たて', 2, 'たて', True),
            '立て(たて)[02]{たて}~'),
    ])
    def test_str(self, name, args, expected):
        word = self.WordClass(*self._default_args(args))

        self.assertEqual(text_type(word), expected)

    @parameterized.expand([
        ('headword', ('を',), ('が',)),
        ('reading',  ('時', 'とき'), ('時', 'じ')),
        ('sense', ('が', None, 3), ('が', None, 2)),
        ('display',
            ('飲ませる', None, None, '飲ませて'),
            ('飲ませる', None, None, '飲ませない')),
        ('example',
            ('ロールプレイング', None, None, None, True),
            ('ロールプレイング', None, None, None, False)),
    ])
    def test_neq(self, name, arg1, arg2):
        w1, w2 = (self.WordClass(*self._default_args(arg))
                  for arg in (arg1, arg2))

        self.assertNotEqual(w1, w2)

    def test_req(self):
        class StrEq(object):
            def __init__(self, base_str):
                self.base_str = base_str

            def __eq__(self, other):
                return text_type(other) == self.base_str

        w = self.WordClass('時', 'とき', None, None, False)

        self.assertTrue(w == StrEq('時(とき)'))
        self.assertTrue(StrEq('時(とき)') == w)

    def test_rneq(self):
        class StrEq(object):
            def __init__(self, base_str):
                self.base_str = base_str

            def __eq__(self, other):
                return text_type(other) == self.base_str

        w = self.WordClass('時', 'とき', None, None, False)

        self.assertFalse(w != StrEq('時(とき)'))
        self.assertFalse(StrEq('時(とき)') != w)


###
# Tatoeba Index Reader tests
class TatoebaIndexReaderTests(ReaderBaseCase):
    _resource_name = 'jpn_indices'
    ReaderClass = tatoeba.TatoebaIndexReader
    WordClass = tatoeba.TanakaWord

    @property
    def sentences(self):
        _sentences = {
            109744: [
                self.WordClass('彼', 'かれ', 1, None, False),
                self.WordClass('は', None, None, None, False),
                self.WordClass('英語', None, None, None, False),
                self.WordClass('が', None, None, None, False),
                self.WordClass('苦手', None, None, None, False),
                self.WordClass('だ', None, None, None, False),
                self.WordClass('が', None, 3, None, False),
                self.WordClass('数学', None, None, None, False),
                self.WordClass('で', None, None, None, False),
                self.WordClass('は', None, None, None, False), 
                self.WordClass('誰にも', None, None, None, False),
                self.WordClass('劣る', None, None, '劣らない', False)
            ],
            112733: [
                self.WordClass('彼', 'かれ', 1, None, False),
                self.WordClass('は', None, None, None, False),
                self.WordClass('其の', None, 1, 'その', False),
                self.WordClass('時', 'とき', None, None, False),
                self.WordClass('大学', None, None, None, False),
                self.WordClass('を', None, None, None, False),
                self.WordClass('卒業', None, 1, None, False),
                self.WordClass('為る', 'する', None, 'し', False),
                self.WordClass('立て', 'たて', 2, 'たて', True),
                self.WordClass('である', None, None, 'であった', False)
            ],
            192227: [
                self.WordClass('ロールプレイング', None, None, None, True),
                self.WordClass('の', None, None, None, False),
                self.WordClass('テレビゲーム', None, None, None, False),
                self.WordClass('は', None, None, None, False),
                self.WordClass('時間', None, None, None, False),
                self.WordClass('を', None, None, None, False),
                self.WordClass('食う', None, 7, None, False)
            ]
        }

        return _sentences

    def test_basic(self):
        ir = self.load_file()

        # A selection of the sentences
        for sent_id, sent in self.sentences.items():
            exp_sent = sent
            act_sent = ir[sent_id]
            self.assertEqual(sent, act_sent)

            # In this case, we're going to make sure that the actual
            # .display property was actually set correctly as well
            for exp_word, act_word in zip(exp_sent, act_sent):
                self.assertEqual(exp_word.display, act_word.display)

    def test_link(self):
        ir = self.load_file()

        links = {
            82526: 321190, 93620: 310087, 109744: 293946, 112733: 290943,
            156245: 258289, 192227: 29390, 199398: 54432, 208975: 46235,
            224758: 62093, 231440: 68807
        }

        for sent_id, link_id in links.items():
            self.assertEqual(link_id, ir.link(sent_id))

    def test_link_error(self):
        ir = self.load_file()

        with self.assertRaises(tatoeba.InvalidIDError):
            ir.link(1224)

    def test_jpn_indices(self):
        ir = self.load_file()

        self.assertEqual(ir.jpn_indices, self.resource_fpath())

    def test_subset(self):
        ir = self.load_file(sentence_ids=(112733, 109744))

        self.assertEqual(len(ir), 2)

        self.assertEqual(ir.sentence_id_subset, {112733, 109744})
        self.assertEqual(set(ir.keys()), {112733, 109744})

class TatoebaIndexReaderEdictTests(TatoebaIndexReaderTests):
    ReaderClass = partial(tatoeba.TatoebaIndexReader, edict=get_edict())
    
    @property
    def sentences(self):
        _sentences = {
            109744: [
                self.WordClass('彼', 'かれ', 1, None, False),
                self.WordClass('は', None, None, None, False),
                self.WordClass('英語', 'えいご', None, None, False),
                self.WordClass('が', None, None, None, False),
                self.WordClass('苦手', 'にがて', None, None, False),
                self.WordClass('だ', None, None, None, False),
                self.WordClass('が', None, 3, None, False),
                self.WordClass('数学', 'すうがく', None, None, False),
                self.WordClass('で', None, None, None, False),
                self.WordClass('は', None, None, None, False), 
                self.WordClass('誰にも', 'だれにも', None, None, False),
                self.WordClass('劣る', 'おとる', None, '劣らない', False)
            ],
            112733: [
                self.WordClass('彼', 'かれ', 1, None, False),
                self.WordClass('は', None, None, None, False),
                self.WordClass('其の', 'その', 1, 'その', False),
                self.WordClass('時', 'とき', None, None, False),
                self.WordClass('大学', 'だいがく', None, None, False),
                self.WordClass('を', None, None, None, False),
                self.WordClass('卒業', 'そつぎょう', 1, None, False),
                self.WordClass('為る', 'する', None, 'し', False),
                self.WordClass('立て', 'たて', 2, 'たて', True),
                self.WordClass('である', None, None, 'であった', False)
            ],
            192227: [
                self.WordClass('ロールプレイング', None, None, None, True),
                self.WordClass('の', None, None, None, False),
                self.WordClass('テレビゲーム', None, None, None, False),
                self.WordClass('は', None, None, None, False),
                self.WordClass('時間', 'じかん', None, None, False),
                self.WordClass('を', None, None, None, False),
                self.WordClass('食う', 'くう', 7, None, False)
            ]
        }

        return _sentences

class TatoebaIndexReaderMiscTests(unittest.TestCase):
    def test_invalid_file(self):
        # First word has display before sense.
        invalid_str = ('93620\t310087\t'
                       '彼女{テレビ}[01] は|1 一時間{１時間} 以内 に 戻る{戻ります}\n')

        with self.assertRaises(tatoeba.InvalidEntryError):
            ir = tatoeba.TatoebaIndexReader(to_string_stream(invalid_str))

