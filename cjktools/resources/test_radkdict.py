# -*- coding: utf-8 -*-
#
#  test_radkdict.py
#  cjktools
#

import unittest
from cStringIO import StringIO

from radkdict import RadkDict


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(RadkdictTestCase)
    ))
    return test_suite

SAMPLE = \
"""
$ 一 1
偏
$ ｜ 1
偏
$ 化 2 js01
偏
$ 冂 2
偏
$ 尸 3
偏
$ 戸 4
偏
$ 冊 5
偏
"""  # nopep8


class RadkdictTestCase(unittest.TestCase):
    def test_fetch_radicals(self):
        key = u'偏'
        rkd = RadkDict(StringIO(SAMPLE))
        radicals = set(rkd[key])
        expected_radicals = set([u'一', u'｜', u'化', u'冂', u'尸', u'戸',
                                 u'冊'])
        self.assertEqual(radicals, expected_radicals)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
