# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testKanaTable.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 16:14:08 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
import kanaTable

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(KanaTableTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class KanaTableTestCase(unittest.TestCase):
    """
    This class tests the Kana class. 
    """
    def setUp(self):
        self.table = kanaTable.KanaTable.getCached()
        self.testScript = u'AＡあア亜'
        pass

    def testVowelLine(self):
        """
        Tests correct vowel line detection.
        """
        self.assertEqual(self.table.toVowelLine(u'ご'), u'お')
        self.assertEqual(self.table.toVowelLine(u'も'), u'お')
        self.assertEqual(self.table.toVowelLine(u'さ'), u'あ')
        self.assertEqual(self.table.toVowelLine(u'あ'), u'あ')
        self.assertEqual(self.table.toVowelLine(u'ぎ'), u'い')

        self.assertEqual(self.table.toVowelLine(u'わ'), u'あ')
        return

    def testConsonantLine(self):
        self.assertEqual(self.table.toConsonantLine(u'わ'), None)

    def testFromCoords(self):
        """Rendering kana from (consonant, vowel) coordinates."""

        self.assertEqual(self.table.fromCoords(u'か', u'お'), u'こ')
        self.assertEqual(self.table.fromCoords(u'ぱ', u'え'), u'ぺ')

    def testIsVoiced(self):
        assert self.table.isVoiced(u'ば')
        assert self.table.isVoiced(u'ぱ')
        assert not self.table.isVoiced(u'は')
        assert self.table.isVoiced(u'だ')
        assert self.table.isVoiced(u'ざ')

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

