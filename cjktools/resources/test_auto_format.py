# -*- coding: utf-8 -*-
#
#  test_auto_format.py
#  cjktools
#

import unittest

from auto_format import detect_format, load_dictionary
from bilingual_dict import BilingualDictionary
import cjkdata


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(AutoFormatTestCase)
    ))
    return test_suite


class AutoFormatTestCase(unittest.TestCase):
    def setUp(self):
        self.je_edict = cjkdata.get_resource('dict/je_edict')
        self.je_jplaces = cjkdata.get_resource('dict/je_jplaces')

    def test_formats(self):
        "Tests correct format detection for a variety of dictionaries."
        self.assertEqual(detect_format(self.je_edict).name, 'edict')
        self.assertEqual(detect_format(self.je_jplaces).name, 'edict')

    def test_edict(self):
        "Tests correct detection and parsing of edict."
        dict_obj = load_dictionary(self.je_edict)
        assert isinstance(dict_obj, BilingualDictionary)
        self.assertEqual(dict_obj.format.name, 'edict')

        self._check_lookup(
            dict_obj,
            u'齧歯目',
            [u'げっしもく'],
            [u'(n) (1) Rodentia', u'(adj-no) (2) rat-like', u'rodential'],
        )

        self._check_lookup(
            dict_obj,
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
