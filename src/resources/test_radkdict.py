# -*- coding: utf-8 -*-
#
#  test_radkdict.py
#  cjktools
#

import unittest
import pkg_resources

from radkdict import RadkDict
from cjktools.scripts import unique_kanji


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(RadkdictTestCase)
    ))
    return test_suite


class RadkdictTestCase(unittest.TestCase):
    def test_construction(self):
        rkd = RadkDict()
        n_kanji = len(unique_kanji(pkg_resources.resource_string(
            'cjktools_data', 'radkfile').decode('utf8')))
        self.assertEqual(len(rkd), n_kanji)

    def test_fetch_radicals(self):
        key = u'偏'
        rkd = RadkDict()
        radicals = set(rkd[key])
        expected_radicals = set([u'一', u'｜', u'化', u'冂', u'尸', u'戸', u'冊'])
        self.assertEqual(radicals, expected_radicals)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
