# -*- coding: utf-8 -*-
#
#  test_auto_format.py
#  cjktools
#
import unittest
import codecs
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from auto_format import detect_format, load_dictionary
from bilingual_dict import BilingualDictionary

from six import text_type, binary_type

def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(AutoFormatTestCase)
    ))
    return test_suite

EDICT_SAMPLE = \
"""　？？？ /EDICT, EDICT_SUB(P), EDICT2 Japanese-English Electronic Dictionary Files/Copyright Electronic Dictionary Research & Development Group - 2011/Created: 2011-07-03/
齧歯目 [げっしもく] /(n) (1) Rodentia/(adj-no) (2) rat-like/rodential/
齲歯 [うし] /(n,adj-no) cavity/tooth decay/decayed tooth/caries/
齲歯 [むしば] /(n,adj-no) cavity/tooth decay/decayed tooth/caries/
"""  # nopep8

JPLACES_SAMPLE = \
"""？？？？ /J_PLACES  A file of Japanese place names compiled from the files from the www.postal.mpt.go.jp site, Dec 1998 version/
秋葉原 [あきはばら] /Akihabara (loc)/
上野 [うえの] /Ueno (loc)/
"""  # nopep8

def _to_unicode_stream(x):
    o = StringIO(x)

    if isinstance(x, binary_type):
        o = codecs.getreader('utf8')(o)

    return o

class AutoFormatTestCase(unittest.TestCase):
    def setUp(self):

        self.je_edict = _to_unicode_stream(EDICT_SAMPLE)
        self.je_jplaces = _to_unicode_stream(JPLACES_SAMPLE)

    def test_formats(self):
        "Tests correct format detection for a variety of dictionaries."
        self.assertEqual(
            detect_format(next(self.je_edict)).name,
            'edict',
        )
        self.assertEqual(
            detect_format(next(self.je_jplaces)).name,
            'edict',
        )

    def test_edict(self):
        "Tests correct detection and parsing of edict."
        d = load_dictionary(self.je_edict)
        assert isinstance(d, BilingualDictionary)
        self.assertEqual(d.format.name, 'edict')

        self.assertEqual(len(d), 2)

        self._check_lookup(
            d,
            u'齧歯目',
            [u'げっしもく'],
            [u'(n) (1) Rodentia', u'(adj-no) (2) rat-like', u'rodential'],
        )

        self._check_lookup(
            d,
            u'齲歯',
            [u'うし']*4 + [u'むしば']*4,
            ['(n,adj-no) cavity', 'tooth decay', 'decayed tooth',
                'caries']*2,
        )

    def _check_lookup(self, dictionary, key, readings, senses):
        entry = dictionary[key]
        self.assertEqual(entry.readings, readings)
        self.assertEqual(entry.senses, senses)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
