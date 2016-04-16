# -*- coding: utf-8 -*-
#
#  test_bilingual_dict.py
#  cjktools
#

from __future__ import unicode_literals

import unittest
from cjktools.resources import bilingual_dict

from cjktools.errors import NotYetImplementedError

from cjktools.resources.dict_format import RegexFormat

edict_fmt = RegexFormat('edict', '^.？？？.*$',
    '^(?P<word>[^ ]+) (\[(?P<reading>[^\]]+)\] )?(?P<senses>.*)$',
    '/(?P<sense>[^/]+)')

class BilingualDictTest(unittest.TestCase):
    def testUpdateDefaultPolicy(self):
        d1 = bilingual_dict.BilingualDictionary(edict_fmt)

        d1['a'] = 2
        d2 = {'a': 4, 'b': 1}

        d1.update(d2)

        self.assertEqual(d1['a'], 4)
        self.assertEqual(d1['b'], 1)

    def testClashPolicyOverwrite(self):
        d1 = bilingual_dict.BilingualDictionary(edict_fmt)

        d1['a'] = 2
        d2 = {'a': 4, 'b': 1}

        d1.update(d2, clash_policy=bilingual_dict.ClashPolicy.Overwrite)

        self.assertEqual(d1['a'], 4)
        self.assertEqual(d1['b'], 1)

    def testClashPolicyMerge(self):
        d1 = bilingual_dict.BilingualDictionary(edict_fmt)

        d1['a'] = 2
        d2 = {'a': 4, 'b': 1}

        with self.assertRaises(NotYetImplementedError):
            clash_policy = bilingual_dict.ClashPolicy.Merge
            d1.update(d2, clash_policy=clash_policy)










