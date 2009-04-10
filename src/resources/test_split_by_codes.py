# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_split_by_codes.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Jun 13 10:38:14 2007
#
#----------------------------------------------------------------------------# 

import unittest
import pkg_resources

from split_by_codes import load_coded_dictionary

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(SplitByCodesTestCase)
        ))
    return test_suite

#----------------------------------------------------------------------------#

class SplitByCodesTestCase(unittest.TestCase):
    """
    This class tests the SplitByCodes class. 
    """
    def setUp(self):
        self.enamdict_file = pkg_resources.resource_filename('cjktools_data', 
                'dict/je_enamdict')
        self.edict_file = pkg_resources.resource_filename('cjktools_data',
                'dict/je_edict')
        pass

    def test_enamdict(self):
        """
        Checks code splitting for enamdict. 
        """
        enamdic_coded = load_coded_dictionary(self.enamdict_file)
        for known_code  in ['u', 'p', 's', 'f', 'm', 'pr', 'st', 'co']:
            assert known_code in enamdic_coded

        assert u'秋葉橋' in enamdic_coded['p']
        assert u'秋葉橋' not in enamdic_coded['s']

        return

    def test_edict(self):
        edict_coded = load_coded_dictionary(self.edict_file)

        assert 'adj' in edict_coded
        adjectives = edict_coded['adj']
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

