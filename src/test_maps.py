# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_maps.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 15:46:00 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
import maps

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(MapTestCases),
            unittest.makeSuite(PartialMapTestCase),
            unittest.makeSuite(MultiDictTestCase),
        ))
    return test_suite

#----------------------------------------------------------------------------#

class MapTestCases(unittest.TestCase):
    def test_chain_dicts(self):
        """
        Tests chaining together dictionaries.
        """
        dataA = {1: 'a', 2: 'b', 3: 'c'}
        dataB = {'a': 1.5, 'b': 3.5, 'c': 1.5}

        self.assertEqual(
                maps.chain_mapping(dataA, dataB),
                {1:1.5, 2:3.5, 3:1.5}
            )

        return

    def test_invert_dict(self):
        """
        Tests inverting a dictionary.
        """
        data = {1: [1,2,3], 2: [1,3]}
        new_dict = maps.invert_mapping(data)
        self.assertEqual(new_dict, {1:[1,2], 2:[1], 3:[1,2]})

        data2 = {1: 'a', 2: 'b', 3: 'c'}
        new_dict2 = maps.invert_injective_mapping(data2)
        self.assertEqual(new_dict2, {'a': 1, 'b': 2, 'c': 3})

        return

    def test_map_dict(self):
        """
        Tests map as applied to dictionaries.
        """
        data = {'a': 1, 'b': 2, 'c': 3}
        method = lambda x: x*x
        new_data = maps.map_dict(method, data)

        self.assertEqual(new_data, {'a': 1, 'b': 4, 'c': 9})
        maps.map_dict(method, data, in_place=True)
        self.assertEqual(data, new_data)

        return

    def test_merge_dicts(self):
        """
        Tests merging multiple dictionaries.
        """
        dictA = {
                    1: set('cat'),
                    2: set('dog'),
                }
        dictB = {
                    1: 'canine',
                    3: 'bird',
                }

        result = maps.merge_dicts(dictA, dictB)

        self.assertEqual(result[1], set('catine'))
        self.assertEqual(result[2], set('dog'))
        self.assertEqual(result[3], set('bird'))

        self.assertEqual(dictA, maps.merge_dicts(dictA, dictA, dictA))

        return

#----------------------------------------------------------------------------#

class PartialMapTestCase(unittest.TestCase):
    def test_to_none(self):
        """
        Everything maps to None
        """
        def to_none(a): return None

        init_list = range(10)
        ok_list, bad_list = maps.partial_map(to_none, init_list)

        assert ok_list == []
        assert bad_list == range(10)

        return
    
    def test_all_ok(self):
        """
        Everthing maps to a true value
        """
        def id(a): return a

        init_list = range(1,11)
        ok_list, bad_list = maps.partial_map(id, init_list)

        assert ok_list == init_list, "Expected: %s, got: %s" % \
                (`init_list`, `ok_list`)
        assert bad_list == []

        return

    def test_partial(self):
        """
        Realistic case, part goes either way
        """
        def kill_even(x):
            if x % 2 == 0:
                return None
            else:
                return x*10

        init_list = range(10, 20)
        ok_list, bad_list = maps.partial_map(kill_even, init_list)
        
        assert ok_list == [110, 130, 150, 170, 190]
        assert bad_list == [10, 12, 14, 16, 18]

        return

#----------------------------------------------------------------------------#

class MultiDictTestCase(unittest.TestCase):
    def test_multi_dict(self):
        """
        A simple maps.multi_dict test case.
        """
        input_pairs = [('a', 2), ('b', 3), ('a', 4)]
        self.assertEqual(maps.multi_dict(input_pairs), {'a': [2,4], 'b': [3]})
        self.assertEqual(maps.multi_dict([]), {})

        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
