# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testScripts.py
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
    testSuite = unittest.TestSuite((
            unittest.makeSuite(ScriptsTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class ScriptsTestCase(unittest.TestCase):
    """This class tests script detection and invariance."""
    def setUp(self):
        self.testScript = u'AＡあア亜'
        pass

    def testFetchScripts(self):
        """
        Test fetching of hiragana and katakana, and converting between them.
        """
        hiragana = u'ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔゕゖ'
        self.assertEqual(scripts.getScript(Script.Hiragana), hiragana)
        katakana = u'ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ'
        self.assertEqual(scripts.getScript(Script.Katakana), katakana)

        self.assertEqual(scripts.toHiragana(katakana), hiragana)
        self.assertEqual(scripts.toKatakana(hiragana), katakana)

        return

    def testScriptType(self):
        """ Tests the scriptType() method.
        """
        scriptType = scripts.scriptType
        self.assertEqual(scriptType(self.testScript), Script.Ascii)
        self.assertEqual(scriptType(self.testScript[1]), Script.FullAscii)
        self.assertEqual(scriptType(self.testScript[2]), Script.Hiragana)
        self.assertEqual(scriptType(self.testScript[3]), Script.Katakana)
        self.assertEqual(scriptType(self.testScript[4]), Script.Kanji)

        return

    def testContainsScript(self):
        """
        Tests the containsScript() method.
        """
        containsScript = scripts.containsScript
        assert containsScript(Script.Hiragana, self.testScript)
        assert containsScript(Script.Kanji, self.testScript)
        assert containsScript(Script.Ascii, self.testScript)
        assert containsScript(Script.Katakana, self.testScript)

        assert not containsScript(Script.Ascii, self.testScript[1:])
        assert not containsScript(Script.Kanji, self.testScript[:-1])

        return

    def testCompareKana(self):
        """
        Tests the compareKana() method.
        """
        assert scripts.compareKana(u'Aあア亜', u'Aアあ亜') == 0
        assert scripts.compareKana(u'あAア亜', u'アあ亜A') != 0
        return

    def testNormalizeAscii(self):
        """
        Tests that ascii characters are normalized correctly.
        """
        fullWidthString = u'ｋｌｉｎｇｏｎｓ　ｏｎ　ｔｈｅ　'\
            u'ｓｔａｒｂｏａｒｄ　ｂｏｗ！＠＃＆＊（）？，。；＋＝"'
        halfWidthString = u'klingons on the starboard bow!@#&*()?,.;+="'

        self.assertEqual(len(fullWidthString), len(halfWidthString))

        for fullChar, halfChar in zip(fullWidthString, halfWidthString):
            self.assertEqual(scripts.normalizeAscii(fullChar), halfChar)

        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

