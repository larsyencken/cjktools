# -*- coding: utf-8 -*-
#
#  test_kanji_list.py
#  cjktools
#

import unittest

from cjktools.resources import kanji_list

from six import text_type

def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(KanjiListTest),
    ))
    return test_suite


class KanjiListTest(unittest.TestCase):
    """This class tests the Tree class."""
    def test_availability(self):
        assert 'jp_jyouyou' in kanji_list.get_lists()

    def test_parsing(self):
        kanji_set = kanji_list.get_list('jp_jyouyou')

        self.assertGreater(len(kanji_set), 0)
        self.assertTrue(all(isinstance(x, text_type) for x in kanji_set))
        self.assertEqual(sum(map(len, kanji_set)), len(kanji_set))


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
