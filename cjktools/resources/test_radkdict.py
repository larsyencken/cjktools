# -*- coding: utf-8 -*-
#
#  test_radkdict.py
#  cjktools
#

import codecs
import unittest

from radkdict import RadkDict
from cjktools.scripts import unique_kanji
import cjkdata


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(RadkdictTestCase)
    ))
    return test_suite


class RadkdictTestCase(unittest.TestCase):
    def test_construction(self):
        rkd = RadkDict()
        f = cjkdata.get_resource('radkfile')
        with codecs.open(f, 'r', 'utf8') as istream:
            data = istream.read()
        n_kanji = len(unique_kanji(data))
        self.assertEqual(len(rkd), n_kanji)

    def test_fetch_radicals(self):
        key = u'偏'
        rkd = RadkDict()
        radicals = set(rkd[key])
        expected_radicals = set([u'一', u'｜', u'化', u'冂', u'尸', u'戸',
                                 u'冊'])
        self.assertEqual(radicals, expected_radicals)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
