# -*- coding: utf-8 -*-
#
#  test_zhuyin_table.py
#  cjktools
#

import re
import unittest
from cStringIO import StringIO

import zhuyin_table


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(ZhuyinTableTestCase)
    ))
    return test_suite


class ZhuyinTableTestCase(unittest.TestCase):
    def setUp(self):
        self.data = \
"""ㄔㄚ cha
ㄅㄟ bei
ㄐㄧㄥ jing
ㄉㄚ da
ㄒㄩㄝ xue
"""  # nopep8

    def test_zhuyin_to_pinyin(self):
        dict_obj = zhuyin_table.zhuyin_to_pinyin_table(
            StringIO(self.data)
        )
        self.assertEqual(dict_obj[u'ㄔㄚ'], u'cha')

    def test_pinyin_to_zhuyin(self):
        dict_obj = zhuyin_table.pinyin_to_zhuyin_table(
            StringIO(self.data)
        )
        self.assertEqual(dict_obj[u'cha'], u'ㄔㄚ')

    def test_pinyin_parsing(self):
        base_pattern = zhuyin_table.pinyin_regex_pattern(
            StringIO(self.data)
        )
        pattern = re.compile(r'^(%s)+$' % base_pattern, re.UNICODE)
        assert not pattern.match(u'gdaymatehowsitgoing')
        assert pattern.match(u'beijingdaxue')


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
