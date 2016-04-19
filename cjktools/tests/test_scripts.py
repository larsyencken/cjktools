# -*- coding: utf-8 -*-
#
#  test_scripts.py
#  cjktools
#

from __future__ import unicode_literals

import unittest

from cjktools import scripts
from cjktools.scripts import Script


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(ScriptsTestCase),
    ))
    return test_suite


class ScriptsTestCase(unittest.TestCase):
    """This class tests script detection and invariance."""
    def setUp(self):
        self.test_script = 'AＡあア亜'
        pass

    def test_fetch_scripts(self):
        """
        Test fetching of hiragana and katakana, and converting between them.
        """
        hiragana = 'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ'  # nopep8
        self.assertEqual(scripts.get_script(Script.Hiragana), hiragana)
        katakana = 'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ'  # nopep8
        self.assertEqual(scripts.get_script(Script.Katakana), katakana)

        self.assertEqual(scripts.to_hiragana(katakana), hiragana)
        self.assertEqual(scripts.to_katakana(hiragana), katakana)

    def test_script_type(self):
        """ Tests the script_type() method.
        """
        script_type = scripts.script_type
        self.assertEqual(script_type(self.test_script), Script.Ascii)
        self.assertEqual(script_type(self.test_script[1]), Script.FullAscii)
        self.assertEqual(script_type(self.test_script[2]), Script.Hiragana)
        self.assertEqual(script_type(self.test_script[3]), Script.Katakana)
        self.assertEqual(script_type(self.test_script[4]), Script.Kanji)

    def test_contains_script(self):
        """
        Tests the contains_script() method.
        """
        contains_script = scripts.contains_script
        self.assertTrue(contains_script(Script.Hiragana, self.test_script))
        self.assertTrue(contains_script(Script.Kanji, self.test_script))
        self.assertTrue(contains_script(Script.Ascii, self.test_script))
        self.assertTrue(contains_script(Script.Katakana, self.test_script))

        self.assertFalse(contains_script(Script.Ascii, self.test_script[1:]))
        self.assertFalse(contains_script(Script.Kanji, self.test_script[:-1]))

    def test_compare_kana(self):
        """
        Tests the compare_kana() method.
        """
        self.assertEqual(scripts.compare_kana('Aあア亜', 'Aアあ亜'), 0)
        self.assertNotEqual(scripts.compare_kana('あAア亜', 'アあ亜A'),  0)

    def test_normalize_ascii(self):
        """
        Tests that ascii characters are normalized correctly.
        """
        full_width_string = 'ｋｌｉｎｇｏｎｓ　ｏｎ　ｔｈｅ　'\
            'ｓｔａｒｂｏａｒｄ　ｂｏｗ！＠＃＆＊（）？，。；＋＝"'
        half_width_string = 'klingons on the starboard bow!@#&*()?,.;+="'

        self.assertEqual(len(full_width_string), len(half_width_string))

        for full_char, half_char in zip(full_width_string, half_width_string):
            self.assertEqual(scripts.normalize_ascii(full_char), half_char)

    def test_normalize_kana(self):
        self.assertEqual(scripts.normalize_kana('ｶｷｸｹｺ'), 'カキクケコ')

    def test_normalize(self):
        self.assertEqual(scripts.normalize('Aあア阿ｱＡ'), 'Aあア阿アA')

    def test_script_type_empty(self):
        self.assertEqual(scripts.script_type(''), scripts.Script.Unknown)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
