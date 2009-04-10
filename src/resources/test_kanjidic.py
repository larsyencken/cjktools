# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_kanjidic.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec  5 17:04:51 2006
#
#----------------------------------------------------------------------------# 

import unittest
from kanjidic import *

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(KanjidicTestCase)
        ))
    return test_suite

#----------------------------------------------------------------------------#

class KanjidicTestCase(unittest.TestCase):
    """
    This class tests the Kanjidic class. 
    """
    def setUp(self):
        self.kd = Kanjidic()
        pass

    def test_lookup(self):
        """
        Tests lookup of some kanji using kanjidic.
        """
        key = u'冊'
        result = self.kd[key]
        self.assertEqual(result.stroke_count, 5)
        self.assertEqual(result.skip_code, (4, 5, 1))

        key = u'悪'
        result = self.kd[key]
        self.assertEqual(result.frequency, 469)

        return

    def test_error_case(self):
        key = u'粉'
        assert u'こ'in self.kd[key].all_readings
        return
    
    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

