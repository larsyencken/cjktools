# -*- coding: utf-8 -*-
#
#  test_zhuyin_table.py
#  cjktools
#

import re
import unittest

import zhuyin_table


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(ZhuyinTableTestCase)
    ))
    return test_suite


class ZhuyinTableTestCase(unittest.TestCase):
    def test_zhuyin_to_pinyin(self):
        dict_obj = zhuyin_table.get_zhuyin_to_pinyin_table()
        self.assertEqual(dict_obj[u'ㄔㄚ'], u'cha')

    def test_pinyin_to_zhuyin(self):
        dict_obj = zhuyin_table.get_pinyin_to_zhuyin_table()
        self.assertEqual(dict_obj[u'cha'], u'ㄔㄚ')

    def test_pinyin_parsing(self):
        base_pattern = zhuyin_table.pinyin_regex_pattern()
        pattern = re.compile(r'^(%s)+$' % base_pattern, re.UNICODE)
        assert not pattern.match(u'gdaymatehowsitgoing')
        assert pattern.match(u'woshangbeijingdaxue')
        assert pattern.match(u'woquguoxianjiapo')


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
