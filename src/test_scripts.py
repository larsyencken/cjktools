# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_scripts.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Jun 26 10:33:54 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
import scripts
from scripts import Script

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(ScriptsTestCase),
        ))
    return test_suite

#----------------------------------------------------------------------------#

class ScriptsTestCase(unittest.TestCase):
    """This class tests script detection and invariance."""
    def setUp(self):
        self.test_script = u'AＡあア亜'
        pass

    def test_fetch_scripts(self):
        """
        Test fetching of hiragana and katakana, and converting between them.
        """
        hiragana = u'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ'
        self.assertEqual(scripts.get_script(Script.Hiragana), hiragana)
        katakana = u'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ'
        self.assertEqual(scripts.get_script(Script.Katakana), katakana)

        self.assertEqual(scripts.to_hiragana(katakana), hiragana)
        self.assertEqual(scripts.to_katakana(hiragana), katakana)

        return

    def test_script_type(self):
        """ Tests the script_type() method.
        """
        script_type = scripts.script_type
        self.assertEqual(script_type(self.test_script), Script.Ascii)
        self.assertEqual(script_type(self.test_script[1]), Script.FullAscii)
        self.assertEqual(script_type(self.test_script[2]), Script.Hiragana)
        self.assertEqual(script_type(self.test_script[3]), Script.Katakana)
        self.assertEqual(script_type(self.test_script[4]), Script.Kanji)

        return

    def test_contains_script(self):
        """
        Tests the contains_script() method.
        """
        contains_script = scripts.contains_script
        assert contains_script(Script.Hiragana, self.test_script)
        assert contains_script(Script.Kanji, self.test_script)
        assert contains_script(Script.Ascii, self.test_script)
        assert contains_script(Script.Katakana, self.test_script)

        assert not contains_script(Script.Ascii, self.test_script[1:])
        assert not contains_script(Script.Kanji, self.test_script[:-1])

        return

    def test_compare_kana(self):
        """
        Tests the compare_kana() method.
        """
        assert scripts.compare_kana(u'Aあア亜', u'Aアあ亜') == 0
        assert scripts.compare_kana(u'あAア亜', u'アあ亜A') != 0
        return

    def test_normalize_ascii(self):
        """
        Tests that ascii characters are normalized correctly.
        """
        full_width_string = u'ｋｌｉｎｇｏｎｓ　ｏｎ　ｔｈｅ　'\
            u'ｓｔａｒｂｏａｒｄ　ｂｏｗ！＠＃＆＊（）？，。；＋＝"'
        half_width_string = u'klingons on the starboard bow!@#&*()?,.;+="'

        self.assertEqual(len(full_width_string), len(half_width_string))

        for full_char, half_char in zip(full_width_string, half_width_string):
            self.assertEqual(scripts.normalize_ascii(full_char), half_char)

        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

