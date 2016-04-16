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
        self.assertTrue(self.table.is_voiced('ば'))
        self.assertTrue(self.table.is_voiced('ぱ'))
        self.assertFalse(self.table.is_voiced('は'))
        self.assertTrue(self.table.is_voiced('だ'))
        self.assertTrue(self.table.is_voiced('ざ'))

    def test_repr(self):
        self.assertEqual(repr(self.table), 'KanaTable()')


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
