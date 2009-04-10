# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_pinyin_table.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 12 10:32:43 2006
#
#----------------------------------------------------------------------------# 

import unittest
from pinyin_table import *
import settings

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(PinyinTableTestCase)
        ))
    return test_suite

#----------------------------------------------------------------------------#

class PinyinTableTestCase(unittest.TestCase):
    """
    This class tests the PinyinTable class. 
    """
    def setUp(self):
        pass

    def test_pinyin_table(self):
        """
        Tests simple conversion from hanzi to unicode pinyin.
        """
        table = get_pinyin_table()
        self.assertEqual(table.from_hanzi(u'一代风流'), u'yīdàifēnglíu')
        return

    def test_ascii_pinyin(self):
        """
        Test simple conversion from ascii to unicode pinyin.
        """
        s = get_pinyin_table()
        self.assertEqual(u'bāolíqǔan', s.from_ascii('bao1li2 quan3'))
        self.assertEqual(u'chéngzhewéiwáng',
                s.from_ascii('cheng2zhewei2wang2'))
        self.assertEqual(u'lǖ', s.from_ascii(u'lü1'))
        return
    
    def test_pinyin_segmenter(self):
        """
        Tests that the segmenter works correctly, and detects tones
        correctly.
        """
        segmenter = get_pinyin_segmenter()
        self.assertEqual(
                segmenter.segment_pinyin('woshangdaxue'),
                (('wo', 0), ('shang', 0), ('da', 0), ('xue', 0)),
            )
        self.assertEqual(
                segmenter.segment_pinyin('wo1shang2da3xue4'),
                (('wo', 1), ('shang', 2), ('da', 3), ('xue', 4)),
            )
        self.assertEqual(
                segmenter.segment_pinyin('cheng2zhewei2wang2'),
                (('cheng', 2), ('zhe', 0), ('wei', 2), ('wang', 2)),
            )
        self.assertEqual(
                segmenter.segment_pinyin('yi1ge4jin4r'),
                (('yi', 1), ('ge', 4), ('jin', 4), ('er', 0))
            )
        self.assertEqual(
                segmenter.segment_pinyin(u'yi1lü4xu'),
                (('yi', 1), (u'lü', 4), (u'xu', 0))
            )
        self.assertEqual(
                segmenter.segment_pinyin(u'yi1lü4xu'),
                (('yi', 1), (u'lü', 4), (u'xu', 0))
            )

        self.assertEqual(
                segmenter.segment_pinyin(u'shangqi3bu4'),
                (('shang', 0), (u'qi', 3), (u'bu', 4))
            )
        return

#    def test_unknown_wildcard(self):
#        """ Tests segmenting with the unknown character wildcard.
#        """
#        segmenter = get_pinyin_segmenter()
#        c = settings.UNKNOWN_WILDCARD
#        self.assertEqual(
#                segmenter.segment_pinyin('gou' + c),
#                (('gou', 0), (c, 0)),
#            )
#        
#        self.assertEqual(
#                segmenter.segment_pinyin(c + 'qi'),
#                ((c, 0), ('qi', 0)),
#            )
#
#        self.assertEqual(
#                segmenter.segment_pinyin(3*c),
#                ((c, 0), (c, 0), (c, 0)),
#            )
#        
#        self.assertEqual(
#                segmenter.segment_pinyin('shang%smen' % c),
#                (('shang', 0), (c, 0), ('men', 0)),
#            )
#        return

    def test_should_fail(self):
        """
        This test should fail with the regex segmenter.
        Build a better segmenter!!!
        """
        segmenter = get_pinyin_segmenter()
        self.assertNotEqual(
                segmenter.segment_pinyin('deniu2'),
                (('de', 0), ('niu', 2))
            )
        return

    def test_strip_tones(self):
        """
        Tests the strip_tones method.
        """
        table = get_pinyin_table()

        # Standard cases
        self.assertEqual(table.strip_tones('xia4wu3hao3'), 'xiawuhao')
        self.assertEqual(table.strip_tones('xia4bu4lai2tai2'), 'xiabulaitai')

        # Uppercase
        self.assertEqual(table.strip_tones('Xia4bu4Lai2tai2'), 'xiabulaitai')

        # Presence of v
        self.assertEqual(table.strip_tones(u'yi1lü4'), u'yilü')

        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

