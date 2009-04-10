# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_auto_format.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 26 11:37:59 2006
#
#----------------------------------------------------------------------------# 

import unittest
from os import path
import pkg_resources

from auto_format import detect_format, load_dictionary
from bilingual_dict import BilingualDictionary

import settings

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(AutoFormatTestCase)
        ))
    return test_suite

#----------------------------------------------------------------------------#

class AutoFormatTestCase(unittest.TestCase):
    """
    This class tests the AutoFormat class. 
    """
    #------------------------------------------------------------------------#

    def setUp(self):
        dict_dir = path.join(settings.get_data_dir(), 'dict')
        self.je_edict = pkg_resources.resource_filename('cjktools_data', 
                'dict/je_edict')
        self.je_jplaces = pkg_resources.resource_filename('cjktools_data', 
                        'dict/je_jplaces')

    #------------------------------------------------------------------------#

    def test_formats(self):
        """
        Tests correct format detection for a variety of dictionaries.
        """
        self.assertEqual(detect_format(self.je_edict).name, 'edict')
        self.assertEqual(detect_format(self.je_jplaces).name, 'edict')
        return

    #------------------------------------------------------------------------#

    def test_edict(self):
        """
        Tests correct detection and parsing of edict.
        """
        dict_obj = load_dictionary(self.je_edict)
        assert isinstance(dict_obj, BilingualDictionary)
        self.assertEqual(dict_obj.format.name, 'edict')

        self._check_lookup(dict_obj,
                u'齧歯目',
                [u'げっしもく'],
                [u'(adj-no) rat-like', u'rhodential'],
            )

        self._check_lookup(dict_obj,
                u'齲歯',
                [u'うし']*4 + [u'むしば']*4,
                ['(n) cavity', 'tooth decay', 'decayed tooth', 'caries']*2,
            )
        return

    #------------------------------------------------------------------------#

    def tearDown(self):
        pass

    #------------------------------------------------------------------------#

    def _check_lookup(self, dictionary, key, readings, senses):
        entry = dictionary[key]
        self.assertEqual(entry.readings, readings)
        self.assertEqual(entry.senses, senses)
        return

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:
