# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_zhuyin_table.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Fri Dec 22 18:02:31 2006
#
#----------------------------------------------------------------------------# 

import re
import unittest

import zhuyin_table

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(ZhuyinTableTestCase)
        ))
    return test_suite

#----------------------------------------------------------------------------#

class ZhuyinTableTestCase(unittest.TestCase):
    """
    This class tests the ZhuyinTable class. 
    """
    def setUp(self):
        pass

    def test_zhuyin_to_pinyin(self):
        dict_obj = zhuyin_table.get_zhuyin_to_pinyin_table()
        self.assertEqual(dict_obj[u'ㄔㄚ'], u'cha')
        return
    
    def test_pinyin_to_zhuyin(self):
        dict_obj = zhuyin_table.get_pinyin_to_zhuyin_table()
        self.assertEqual(dict_obj[u'cha'], u'ㄔㄚ')
        return

    def test_pinyin_parsing(self):
        base_pattern = zhuyin_table.pinyin_regex_pattern()
        pattern = re.compile(r'^(%s)+$' % base_pattern, re.UNICODE)
        assert not pattern.match(u'gdaymatehowsitgoing')
        assert pattern.match(u'woshangbeijingdaxue')
        assert pattern.match(u'woquguoxianjiapo')
        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

