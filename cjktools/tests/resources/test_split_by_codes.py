# -*- coding: utf-8 -*-
#
#  test_split_by_codes.py
#  cjktools
#

import unittest
import codecs
from cStringIO import StringIO

from split_by_codes import load_coded_dictionary


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(SplitByCodesTestCase)
    ))
    return test_suite

ENAMDICT_SAMPLE = \
"""？？？？ /ENAMDICT - Japanese Proper Name Dictionary File/Copyright Electronic Dictionary Research & Development Group, Monash University, 2007/Created: 2011-07-03/
秋葉橋 [あきはばし] /Akihabashi (p)/
秋葉橋 [あきばばし] /Akibabashi (p)/
"""  # nopep8

EDICT_SAMPLE = \
"""　？？？ /EDICT, EDICT_SUB(P), EDICT2 Japanese-English Electronic Dictionary Files/Copyright Electronic Dictionary Research & Development Group - 2011/Created: 2011-07-03/
素晴らしい [すばらしい] /(adj-i) wonderful/splendid/magnificent/(P)/
素晴らしい [すんばらしい] /(adj-i) wonderful/splendid/magnificent/
"""  # nopep8


class SplitByCodesTestCase(unittest.TestCase):
    def test_enamdict(self):
        "Checks code splitting for enamdict."
        enamdic_coded = load_coded_dictionary(
            codecs.getreader('utf8')(StringIO(ENAMDICT_SAMPLE))
        )
        assert 'p' in enamdic_coded
        assert u'秋葉橋' in enamdic_coded['p']
        assert u'秋葉橋' not in enamdic_coded['s']

    def test_edict(self):
        edict_coded = load_coded_dictionary(
            codecs.getreader('utf8')(StringIO(EDICT_SAMPLE))
        )
        assert 'adj-i' in edict_coded
        adjectives = edict_coded['adj-i']
        assert u'素晴らしい' in adjectives
        subarashii = adjectives[u'素晴らしい']
        assert subarashii.readings[0] == u'すばらしい'
        assert subarashii.readings[-1] == u'すんばらしい'


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
