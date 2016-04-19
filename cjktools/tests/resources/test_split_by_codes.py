# -*- coding: utf-8 -*-
#
#  test_split_by_codes.py
#  cjktools
#
from __future__ import unicode_literals

import unittest

from cjktools.resources.split_by_codes import load_coded_dictionary

from .._common import to_unicode_stream


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
            to_unicode_stream(ENAMDICT_SAMPLE)
        )
        self.assertIn('p', enamdic_coded)
        self.assertIn('秋葉橋', enamdic_coded['p'])
        self.assertNotIn('秋葉橋', enamdic_coded['s'])

    def test_edict(self):
        edict_coded = load_coded_dictionary(
            to_unicode_stream(EDICT_SAMPLE)
        )

        self.assertIn('adj-i', edict_coded)

        adjectives = edict_coded['adj-i']
        self.assertIn('素晴らしい', adjectives)

        subarashii = adjectives[u'素晴らしい']
        self.assertEqual(subarashii.readings[0], 'すばらしい')
        self.assertEqual(subarashii.readings[-1], 'すんばらしい')


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
