# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testPinyinTable.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 12 10:32:43 2006
#
#----------------------------------------------------------------------------# 

import unittest
from pinyinTable import *
import settings

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(PinyinTableTestCase)
        ))
    return testSuite

#----------------------------------------------------------------------------#

class PinyinTableTestCase(unittest.TestCase):
    """
    This class tests the PinyinTable class. 
    """
    def setUp(self):
        pass

    def testPinyinTable(self):
        """
        Tests simple conversion from hanzi to unicode pinyin.
        """
        table = getPinyinTable()
        self.assertEqual(table.fromHanzi(u'一代风流'), u'yīdàifēnglíu')
        return

    def testAsciiPinyin(self):
        """
        Test simple conversion from ascii to unicode pinyin.
        """
        s = getPinyinTable()
        self.assertEqual(u'bāolíqǔan', s.fromAscii('bao1li2 quan3'))
        self.assertEqual(u'chéngzhewéiwáng',
                s.fromAscii('cheng2zhewei2wang2'))
        self.assertEqual(u'lǖ', s.fromAscii(u'lü1'))
        return
    
    def testPinyinSegmenter(self):
        """
        Tests that the segmenter works correctly, and detects tones
        correctly.
        """
        segmenter = getPinyinSegmenter()
        self.assertEqual(
                segmenter.segmentPinyin('woshangdaxue'),
                (('wo', 0), ('shang', 0), ('da', 0), ('xue', 0)),
            )
        self.assertEqual(
                segmenter.segmentPinyin('wo1shang2da3xue4'),
                (('wo', 1), ('shang', 2), ('da', 3), ('xue', 4)),
            )
        self.assertEqual(
                segmenter.segmentPinyin('cheng2zhewei2wang2'),
                (('cheng', 2), ('zhe', 0), ('wei', 2), ('wang', 2)),
            )
        self.assertEqual(
                segmenter.segmentPinyin('yi1ge4jin4r'),
                (('yi', 1), ('ge', 4), ('jin', 4), ('er', 0))
            )
        self.assertEqual(
                segmenter.segmentPinyin(u'yi1lü4xu'),
                (('yi', 1), (u'lü', 4), (u'xu', 0))
            )
        self.assertEqual(
                segmenter.segmentPinyin(u'yi1lü4xu'),
                (('yi', 1), (u'lü', 4), (u'xu', 0))
            )

        self.assertEqual(
                segmenter.segmentPinyin(u'shangqi3bu4'),
                (('shang', 0), (u'qi', 3), (u'bu', 4))
            )
        return

#    def testUnknownWildcard(self):
#        """ Tests segmenting with the unknown character wildcard.
#        """
#        segmenter = getPinyinSegmenter()
#        c = settings.UNKNOWN_WILDCARD
#        self.assertEqual(
#                segmenter.segmentPinyin('gou' + c),
#                (('gou', 0), (c, 0)),
#            )
#        
#        self.assertEqual(
#                segmenter.segmentPinyin(c + 'qi'),
#                ((c, 0), ('qi', 0)),
#            )
#
#        self.assertEqual(
#                segmenter.segmentPinyin(3*c),
#                ((c, 0), (c, 0), (c, 0)),
#            )
#        
#        self.assertEqual(
#                segmenter.segmentPinyin('shang%smen' % c),
#                (('shang', 0), (c, 0), ('men', 0)),
#            )
#        return

    def testShouldFail(self):
        """
        This test should fail with the regex segmenter.
        Build a better segmenter!!!
        """
        segmenter = getPinyinSegmenter()
        self.assertNotEqual(
                segmenter.segmentPinyin('deniu2'),
                (('de', 0), ('niu', 2))
            )
        return

    def testStripTones(self):
        """
        Tests the stripTones method.
        """
        table = getPinyinTable()

        # Standard cases
        self.assertEqual(table.stripTones('xia4wu3hao3'), 'xiawuhao')
        self.assertEqual(table.stripTones('xia4bu4lai2tai2'), 'xiabulaitai')

        # Uppercase
        self.assertEqual(table.stripTones('Xia4bu4Lai2tai2'), 'xiabulaitai')

        # Presence of v
        self.assertEqual(table.stripTones(u'yi1lü4'), u'yilü')

        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

