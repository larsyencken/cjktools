# -*- coding: utf-8 -*-
#
#  test_split_by_codes.py
#  cjktools
#

import unittest

from split_by_codes import load_coded_dictionary
import cjkdata


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(SplitByCodesTestCase)
    ))
    return test_suite


class SplitByCodesTestCase(unittest.TestCase):
    def setUp(self):
        self.enamdict_file = cjkdata.get_resource('dict/je_enamdict')
        self.edict_file = cjkdata.get_resource('dict/je_edict')

    def test_enamdict(self):
        "Checks code splitting for enamdict."
        enamdic_coded = load_coded_dictionary(self.enamdict_file)
        for known_code in ['u', 'p', 's', 'f', 'm', 'pr', 'st', 'co']:
            assert known_code in enamdic_coded

        assert u'秋葉橋' in enamdic_coded['p']
        assert u'秋葉橋' not in enamdic_coded['s']

    def test_edict(self):
        edict_coded = load_coded_dictionary(self.edict_file)
        assert 'adj-i' in edict_coded
        adjectives = edict_coded['adj-i']
        assert u'素晴らしい' in adjectives
        subarashii = adjectives[u'素晴らしい']
        assert subarashii.readings[0] == u'すばらしい'
        assert subarashii.readings[-1] == u'すんばらしい'


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
