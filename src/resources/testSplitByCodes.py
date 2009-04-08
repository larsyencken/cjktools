# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testSplitByCodes.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Jun 13 10:38:14 2007
#
#----------------------------------------------------------------------------# 

import unittest
import pkg_resources

from splitByCodes import loadCodedDictionary

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(SplitByCodesTestCase)
        ))
    return testSuite

#----------------------------------------------------------------------------#

class SplitByCodesTestCase(unittest.TestCase):
    """
    This class tests the SplitByCodes class. 
    """
    def setUp(self):
        self.enamdictFile = pkg_resources.resource_filename('cjktools_data', 
                'dict/je_enamdict')
        self.edictFile = pkg_resources.resource_filename('cjktools_data',
                'dict/je_edict')
        pass

    def testEnamdict(self):
        """
        Checks code splitting for enamdict. 
        """
        enamdicCoded = loadCodedDictionary(self.enamdictFile)
        for knownCode  in ['u', 'p', 's', 'f', 'm', 'pr', 'st', 'co']:
            assert knownCode in enamdicCoded

        assert u'秋葉橋' in enamdicCoded['p']
        assert u'秋葉橋' not in enamdicCoded['s']

        return

    def testEdict(self):
        edictCoded = loadCodedDictionary(self.edictFile)

        assert 'adj' in edictCoded
        adjectives = edictCoded['adj']
        assert u'素晴らしい' in adjectives
        subarashii = adjectives[u'素晴らしい']
        assert subarashii.readings[0] == u'すばらしい'
        assert subarashii.readings[-1] == u'すんばらしい'

        return
    
    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

