# -*- coding: utf-8 -*-
#
#  testKanjiList.py
#  unknown project
# 
#  Created by Lars Yencken on 08-04-2009.
#  Copyright 2009 Lars Yencken. All rights reserved.
#

import unittest

import kanjiList

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(KanjiListTest),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class KanjiListTest(unittest.TestCase):
    """This class tests the Tree class."""

    def setUp(self):
        pass
        
    def testAvailability(self):
        assert 'jp_jyouyou' in kanjiList.getLists()
    
    def testParsing(self):
        kanji_set = kanjiList.getList('jp_jyouyou')
        assert len(kanji_set) > 0
        assert set(map(type, kanji_set)) == set([unicode])
        assert sum(map(len, kanji_set)) == len(kanji_set)

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

# vim: ts=4 sw=4 sts=4 et tw=78:

