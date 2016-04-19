# -*- coding: utf-8 -*-
#
#  test_kanjidic.py
#

from __future__ import unicode_literals

import unittest
from cjktools.resources.kanjidic import Kanjidic


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(KanjidicTestCase)
    ))
    return test_suite


class KanjidicTestCase(unittest.TestCase):
    def setUp(self):
        self.kd = Kanjidic()

    def test_get_cached(self):
        kd = Kanjidic.get_cached()

        self.assertIsInstance(kd, Kanjidic)

        kd2 = Kanjidic.get_cached()

        self.assertIs(kd, kd2)

    def test_lookup(self):
        """ Tests lookup of some kanji using kanjidic. """
        key = '冊'
        result = self.kd[key]
        self.assertEqual(result.stroke_count, 5)
        self.assertEqual(result.skip_code, (4, 5, 1))

        key = '悪'
        result = self.kd[key]
        self.assertEqual(result.frequency, 530)

    def test_error_case(self):
        key = '粉'
        self.assertIn('こ', self.kd[key].all_readings)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
