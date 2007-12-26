# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testZhuyinTable.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Fri Dec 22 18:02:31 2006
#
#----------------------------------------------------------------------------# 

import unittest
from zhuyinTable import *

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(ZhuyinTableTestCase)
        ))
    return testSuite

#----------------------------------------------------------------------------#

class ZhuyinTableTestCase(unittest.TestCase):
    """
    This class tests the ZhuyinTable class. 
    """
    def setUp(self):
        pass

    def testZhuyinToPinyin(self):
        dictObj = getZhuyinToPinyinTable()
        self.assertEqual(dictObj[u'ㄔㄚ'], u'cha')
        return
    
    def testPinyinToZhuyin(self):
        dictObj = getPinyinToZhuyinTable()
        self.assertEqual(dictObj[u'cha'], u'ㄔㄚ')
        return

    def testPinyinParsing(self):
        basePattern = pinyinRegexPattern()
        pattern = re.compile(r'^(%s)+$' % basePattern, re.UNICODE)
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

