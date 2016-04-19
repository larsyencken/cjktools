# -*- coding: utf-8 -*-
#
#  test_kana_table.py
#  cjktools
#

from __future__ import unicode_literals

import unittest
from cjktools import kana_table


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(KanaTableTestCase),
    ))
    return test_suite


class KanaTableTestCase(unittest.TestCase):
    def setUp(self):
        self.table = kana_table.KanaTable.get_cached()
        self.test_script = 'AＡあア亜'

    def test_get_coords(self):
        new_table = kana_table.KanaTable()

        for table in (self.table, new_table):
            self.assertEqual(table.get_coords('ち'), ('た', 'い'))
            self.assertEqual(table.get_coords('ぷ'), ('ぱ', 'う'))
            self.assertEqual(table.get_coords('お'), ('あ', 'お'))

    def test_vowel_line(self):
        """
        Tests correct vowel line detection.
        """
        self.assertEqual(self.table.to_vowel_line(u'ご'), u'お')
        self.assertEqual(self.table.to_vowel_line(u'も'), u'お')
        self.assertEqual(self.table.to_vowel_line(u'さ'), u'あ')
        self.assertEqual(self.table.to_vowel_line(u'あ'), u'あ')
        self.assertEqual(self.table.to_vowel_line(u'ぎ'), u'い')

        self.assertEqual(self.table.to_vowel_line(u'わ'), u'あ')

    def test_consonant_line(self):
        self.assertEqual(self.table.to_consonant_line(u'わ'), None)

    def test_from_coords(self):
        """Rendering kana from (consonant, vowel) coordinates."""

        self.assertEqual(self.table.from_coords(u'か', u'お'), u'こ')
        self.assertEqual(self.table.from_coords(u'ぱ', u'え'), u'ぺ')

    def test_is_voiced(self):
        po_composed = 'ほ' + '\u309a'
        vu_composed = 'う' + '\u3099'
        ji_composed = 'し' + '\u3099'
        bad_composed = 'ま' + '\u3099'    # Still should show up voiced

        composed_chars = (po_composed,
                          vu_composed,
                          ji_composed,
                          bad_composed)

        voiced_chars = tuple('ばだゔざ')
        semivoiced_chars = tuple('ぱ')

        for v in (voiced_chars + semivoiced_chars + composed_chars):
            self.assertTrue(self.table.is_voiced(v), v)

        for nv in tuple('はしもにちゃ'):
            self.assertFalse(self.table.is_voiced(nv), nv)

    def test_is_semivoiced(self):
        po_composed = ('ほ' + '\u309a', )
        bo_composed = ('ほ' + '\u3099', )
        for sv in tuple('ぱぽぺぴぷパペピプポ') + po_composed:
            self.assertTrue(self.table.is_semivoiced(sv), sv)

        for nsv in tuple('まかにじばぼびサツズシホハABCç') + bo_composed:
            self.assertFalse(self.table.is_semivoiced(nsv), nsv)

    def test_repr(self):
        self.assertEqual(repr(self.table), 'KanaTable()')


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
