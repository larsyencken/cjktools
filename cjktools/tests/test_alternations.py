# -*- coding: utf-8 -*-
#
#  test_alternations.py
#  cjktools
#

from __future__ import unicode_literals

import unittest
import doctest
from cjktools import alternations

from itertools import product


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(AlternationsTestCase),
        doctest.DocTestSuite(alternations),
    ))
    return test_suite


class AlternationsTestCaseHiragana(unittest.TestCase):
    def test_canonical_forms(self):
        base = ('ゆっ', 'ぐり')
        seg1Cases = ['ゆ' + c for c in 'いちりきつくっ']
        seg2Cases = ['くり', 'ぐり']
        expected = set(product(seg1Cases, seg2Cases))

        self.assertEqual(set(alternations.canonical_forms(base)), expected)

    def test_canonical_segment_forms(self):
        voiced = 'ばり'
        expected = set(['ばり', 'はり'])
        result = set(alternations.canonical_segment_forms(voiced, True, False))
        self.assertEqual(result, expected)

        self.assertEqual(alternations.canonical_segment_forms('わ'),
                         set(['わ']))

    def test_canonical_segment_forms_doubling(self):
        doubled = 'さっ'

        actual = alternations.canonical_segment_forms(doubled, True, True)
        expected = {'さい', 'さき', 'さく', 'さち', 'さっ', 'さつ', 'さり'}

        self.assertEqual(actual, expected)

    def test_surface_forms(self):
        plan = ('けい', 'かく')
        expected = [('けい', 'がく'),
                    ('けい', 'かく'),
                    ('けっ', 'がく'),
                    ('けっ', 'かく')]

        self.assertEqual(set(alternations.surface_forms(plan)),
                         set(expected))

    def test_expand_long_vowels(self):
        # Skipping 'けー' and 'そー' unclear what to do there
        expected = ['すう', 'しい', 'かあ', ]
        long_vowels = ('すー', 'しー', 'かー', )

        for i, e in zip(long_vowels, expected):
            out = alternations.expand_long_vowels(i)
            self.assertEqual(out, e)

class AlternationsTestCaseKatagana(unittest.TestCase):
    # Can probably get more clever about this by parameterizing
    @unittest.skip('Known failure')
    def test_canonical_forms(self):
        base = ('ユッ', 'グリ')
        seg1Cases = ['ユ' + c for c in 'イチリキツクッ']
        seg2Cases = ['クリ', 'グリ']
        expected = set(product(seg1Cases, seg2Cases))

        self.assertEqual(set(alternations.canonical_forms(base)), expected)

    @unittest.skip('Known failure')
    def test_canonical_segment_forms(self):
        voiced = 'バリ'
        expected = set(['バリ', 'ハリ'])
        result = set(alternations.canonical_segment_forms(voiced, True, False))
        self.assertEqual(result, expected)

        self.assertEqual(alternations.canonical_segment_forms('ワ'),
                         set(['ワ']))

    @unittest.skip('Known failure')
    def test_canonical_segment_forms_doubling(self):
        doubled = 'サッ'

        actual = alternations.canonical_segment_forms(doubled, True, True)
        expected = {'サイ', 'サキ', 'サク', 'サチ', 'サッ', 'サツ', 'サリ'}

        self.assertEqual(actual, expected)

    def test_surface_forms(self):
        plan = ('ケイ', 'カク')
        expected = [('ケイ', 'ガク'),
                    ('ケイ', 'カク'),
                    ('ケッ', 'ガク'),
                    ('ケッ', 'カク')]

        self.assertEqual(set(alternations.surface_forms(plan)), set(expected))

    def test_expand_long_vowels(self):
        # Skipping 'ケー' and 'ソー' unclear what to do there
        expected = ['スウ', 'シイ', 'カア', ]
        long_vowels = ('スー', 'シー', 'カー', )

        for i, e in zip(long_vowels, expected):
            out = alternations.expand_long_vowels(i)
            self.assertEqual(out, e)


class AlternationsTestCase(unittest.TestCase):
    def test_insert_duplicate_kanji(self):
        shorthand = '孜々'

        actual = alternations.insert_duplicate_kanji(shorthand)
        expected = '孜孜'
        self.assertEqual(actual, expected)

    def test_expand_long_vowels_mixed(self):
        long_mixed = 'ABCキーさー白い'
        expected = 'ABCキイさあ白い'

        actual = alternations.expand_long_vowels(long_mixed)

        self.assertEqual(actual, expected)

    def test_expand_long_vowels_empty(self):
        empty = ''
        expected = ''

        actual = alternations.expand_long_vowels(empty)

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
