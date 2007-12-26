# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testMaps.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 15:46:00 2007
#
#----------------------------------------------------------------------------# 

import unittest
import doctest
import maps

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(MapTestCases),
            unittest.makeSuite(PartialMapTestCase),
            unittest.makeSuite(MultiDictTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class MapTestCases(unittest.TestCase):
    def testChainDicts(self):
        """
        Tests chaining together dictionaries.
        """
        dataA = {1: 'a', 2: 'b', 3: 'c'}
        dataB = {'a': 1.5, 'b': 3.5, 'c': 1.5}

        self.assertEqual(
                maps.chainMapping(dataA, dataB),
                {1:1.5, 2:3.5, 3:1.5}
            )

        return

    def testInvertDict(self):
        """
        Tests inverting a dictionary.
        """
        data = {1: [1,2,3], 2: [1,3]}
        newDict = maps.invertMapping(data)
        self.assertEqual(newDict, {1:[1,2], 2:[1], 3:[1,2]})

        data2 = {1: 'a', 2: 'b', 3: 'c'}
        newDict2 = maps.invertInjectiveMapping(data2)
        self.assertEqual(newDict2, {'a': 1, 'b': 2, 'c': 3})

        return

    def testMapDict(self):
        """
        Tests map as applied to dictionaries.
        """
        data = {'a': 1, 'b': 2, 'c': 3}
        method = lambda x: x*x
        newData = maps.mapDict(method, data)

        self.assertEqual(newData, {'a': 1, 'b': 4, 'c': 9})
        maps.mapDict(method, data, inPlace=True)
        self.assertEqual(data, newData)

        return

    def testMergeDicts(self):
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

        result = maps.mergeDicts(dictA, dictB)

        self.assertEqual(result[1], set('catine'))
        self.assertEqual(result[2], set('dog'))
        self.assertEqual(result[3], set('bird'))

        self.assertEqual(dictA, maps.mergeDicts(dictA, dictA, dictA))

        return

#----------------------------------------------------------------------------#

class PartialMapTestCase(unittest.TestCase):
    def testToNone(self):
        """
        Everything maps to None
        """
        def toNone(a): return None

        initList = range(10)
        okList, badList = maps.partialMap(toNone, initList)

        assert okList == []
        assert badList == range(10)

        return
    
    def testAllOk(self):
        """
        Everthing maps to a true value
        """
        def id(a): return a

        initList = range(1,11)
        okList, badList = maps.partialMap(id, initList)

        assert okList == initList, "Expected: %s, got: %s" % \
                (`initList`, `okList`)
        assert badList == []

        return

    def testPartial(self):
        """
        Realistic case, part goes either way
        """
        def killEven(x):
            if x % 2 == 0:
                return None
            else:
                return x*10

        initList = range(10, 20)
        okList, badList = maps.partialMap(killEven, initList)
        
        assert okList == [110, 130, 150, 170, 190]
        assert badList == [10, 12, 14, 16, 18]

        return

#----------------------------------------------------------------------------#

class MultiDictTestCase(unittest.TestCase):
    def testMultiDict(self):
        """
        A simple maps.multiDict test case.
        """
        inputPairs = [('a', 2), ('b', 3), ('a', 4)]
        self.assertEqual(maps.multiDict(inputPairs), {'a': [2,4], 'b': [3]})
        self.assertEqual(maps.multiDict([]), {})

        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
