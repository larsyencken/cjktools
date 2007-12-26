# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testSequences.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 15:14:02 2007
#
#----------------------------------------------------------------------------#

import unittest
import doctest
import sequences

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(MiscTestCases),
            unittest.makeSuite(ThreadingTestCase),
            unittest.makeSuite(ZipWithTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class MiscTestCases(unittest.TestCase):
    def testSeparate(self):
        """
        Basic use of separate()
        """
        def isEven(i):
            return i % 2 == 0

        initList = range(10)
        even, odd = sequences.separate(isEven, initList)
        
        assert even == [0,2,4,6,8]
        assert odd == [1,3,5,7,9]

        return

    def testFlatten(self):
        data = [[1,2],3,[[4,[5,[]]]],[], set([1,2,3])]
        self.assertEqual(sequences.flatten(data), [1,2,3,4,5,1,2,3])
        self.assertEqual(list(sequences.iflatten(data)), [1,2,3,4,5,1,2,3])
        return

    def testUnzip(self):
        """
        Tests the unzip method.
        """
        data = zip(range(0, 5), range(4,9))
        unzippedData = sequences.unzip(data)
        self.assertEqual(unzippedData[0], range(0,5))
        self.assertEqual(unzippedData[1], range(4,9))

        return

#----------------------------------------------------------------------------#

class ThreadingTestCase(unittest.TestCase):
    def testThread(self):
        """
        Tests the variety of thread/unthread methods.
        """
        inputPairs = range(6)
        threadedPairs = sequences.thread(inputPairs)
        self.assertEqual(threadedPairs, [(0,1), (2,3), (4,5)])
        self.assertEqual(sequences.unthread(threadedPairs), inputPairs)
        return

#----------------------------------------------------------------------------#

class ZipWithTestCase(unittest.TestCase):
    def testBasic(self):
        """
        Tests basic functioning of the zipWith method.
        """
        inputA = [1,-5, 0]
        inputB = [2, 5, 1]
        method = lambda x, y: x+y

        self.assertEqual(sequences.zipWith(method, inputA, inputB), [3, 0, 1])
        self.assertEqual(
                list(sequences.izipWith(method, inputA, inputB)),
                [3, 0, 1]
            )
        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#
