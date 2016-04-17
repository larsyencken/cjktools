# -*- coding: utf-8 -*-
#
#  test_pinyin_table.py
#  cjktools
#

from __future__ import unicode_literals

import unittest
from cjktools.resources import pinyin_table


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(PinyinTableTestCase)
    ))
    return test_suite


class PinyinTableTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_pinyin_table(self):
        # Tests simple conversion from hanzi to unicode pinyin.
        table = pinyin_table.get_pinyin_table()
        self.assertEqual(table.from_hanzi('一代风流'), 'yīdàifēnglíu')

    def test_ascii_pinyin(self):
        # Test simple conversion from ascii to unicode pinyin.
        s = pinyin_table.get_pinyin_table()
        self.assertEqual('bāolíqǔan', s.from_ascii('bao1li2 quan3'))
        self.assertEqual('chéngzhewéiwáng',
                         s.from_ascii('cheng2zhewei2wang2'))
        self.assertEqual('lǖ', s.from_ascii('lü1'))

    def test_pinyin_segmenter(self):
        # Tests for correct segmentation and tones detection.
        segmenter = pinyin_table.get_pinyin_segmenter()

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
            segmenter.segment_pinyin('yi1lü4xu'),
            (('yi', 1), ('lü', 4), ('xu', 0))
        )

        self.assertEqual(
            segmenter.segment_pinyin('shangqi3bu4'),
            (('shang', 0), ('qi', 3), ('bu', 4))
        )

    @unittest.skip('Known failure: fails with regex segementer')
    def test_garden_path_pinyin(self):
        """
        deniu2 is unambiguously 'de0niu2', but because 'de' and 'ni' are
        valid syllables, they get consumed first and 'u' is not detected.

        The regex segmenter does not handle this situation properly.
        """
        segmenter = pinyin_table.get_pinyin_segmenter()
        self.assertEqual(
            segmenter.segment_pinyin('deniu2'),
            (('de', 0), ('niu', 2))
        )

    def test_strip_tones(self):
        table = pinyin_table.get_pinyin_table()

        # Standard cases
        self.assertEqual(table.strip_tones('xia4wu3hao3'), 'xiawuhao')
        self.assertEqual(table.strip_tones('xia4bu4lai2tai2'), 'xiabulaitai')

        # Uppercase
        self.assertEqual(table.strip_tones('Xia4bu4Lai2tai2'), 'xiabulaitai')

        # Presence of v
        self.assertEqual(table.strip_tones('yi1lü4'), 'yilü')

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
