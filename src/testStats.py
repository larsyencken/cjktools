# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testStats.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Feb 20 18:01:32 EST 2006
#
#----------------------------------------------------------------------------#

import sys, unittest
import doctest
from stats import *

#----------------------------------------------------------------------------#

def suite():
    import stats
    testSuite = unittest.TestSuite((
            unittest.makeSuite(KappaTest),
            unittest.makeSuite(CombinationTest),
            unittest.makeSuite(BasicStatsTest),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class BasicStatsTest(unittest.TestCase):
    def setUp(self):
        self.dataA = [1,2,3]
        self.meanA = 2.0
        self.stddevA = 1.0

        self.dataB = [-50.4, 30.2, 0.1, 4.327]
        self.meanB = -3.94325
        self.stddevB = 33.70824
        return

    def testMean(self):
        """
        Check that mean works as expected.
        """
        self.assertAlmostEqual(mean(self.dataA), self.meanA, 5)
        self.assertAlmostEqual(mean(self.dataB), self.meanB, 5)
        return

    def testBinsByData(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,7,3,0]

        expectedLabels = [(0,3), (3,5), (5,7)]
        expectedBins = [[0,1,2], [3,3], [5,7]]

        self.assertEqual(
                list(binsByData(data, 3)),
                zip(expectedLabels, expectedBins)
            )

        return

    def testBinsByRange(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,9,3,0]

        expectedLabels = [(0.0,3.0), (3.0,6.0), (6.0,9.0)]
        expectedBins = [[0,1,2], [3,3,5], [9]]

        self.assertEqual(
                list(binsByRange(data, 3, lambda x: x)),
                zip(expectedLabels, expectedBins)
            )

        return

    def testBinsByInc(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,8,3,0]

        expectedLabels = [(0.0,3.0), (3.0,6.0), (6.0,9.0)]
        expectedBins = [[0,1,2], [3,3,5], [8]]

        self.assertEqual(
                list(binsByIncrement(data, 3.0, lambda x: x)),
                zip(expectedLabels, expectedBins)
            )

        data = [3,2,5,1,9,3,0]

        expectedLabels = [(0.0,3.0), (3.0,6.0), (6.0,9.0), (9.0, 12.0)]
        expectedBins = [[0,1,2], [3,3,5], [], [9]]

        self.assertEqual(
                list(binsByIncrement(data, 3.0, lambda x: x)),
                zip(expectedLabels, expectedBins)
            )

        return

    def testBadStddev(self):
        """
        Check stddev on a list of length 0.
        """
        try:
            stddev([])
        except:
            pass
        else:
            assert False, "Stddev didn't raise an exception on an empty list"

        return

    def testStddev(self):
        """
        Check that stddev works as expected.
        """
        self.assertAlmostEqual(stddev(self.dataA), self.stddevA, 5)
        self.assertAlmostEqual(stddev(self.dataB), self.stddevB, 5)
        return

    def testOnTuples(self):
        """
        Checks that methods also work on tuples.
        """
        self.assertAlmostEqual(mean(tuple(self.dataA)), self.meanA, 5)
        self.assertAlmostEqual(mean(tuple(self.dataB)), self.meanB, 5)
        self.assertAlmostEqual(stddev(tuple(self.dataA)), self.stddevA, 5)
        self.assertAlmostEqual(stddev(tuple(self.dataB)), self.stddevB, 5)
        return

    def testBasicStats(self):
        """
        Test that the basic stats method works.
        """
        meanA, stddevA = basicStats(self.dataA)
        self.assertAlmostEqual(meanA, mean(self.dataA))
        self.assertAlmostEqual(stddevA, stddev(self.dataA))
        return

    def testSegmentCombinations(self):
        result = set([('d', 'o', 'g'), ('do', 'g'), ('d', 'og'), ('dog',)])
        self.assertEqual(
                set(segmentCombinations(['d', 'o', 'g'])),
                result
            )
        self.assertEqual(
                set(isegmentCombinations(['d', 'o', 'g'])),
                result
            )

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

class KappaTest(unittest.TestCase):
    def setUp(self):
        self.dataA = [1, 2, 3, 4]
        self.dataB = [2, 3, 4, 5]

    def testHighKappa(self):
        """
        Tests a high kappa value
        """
        kappaVal = kappa(self.dataA, self.dataA)
        self.assertAlmostEqual(kappaVal, 1.0)
        return
    
    def testNoAgreement(self):
        """
        Tests the no agreement case.
        """
        kappaVal = kappa(self.dataA, self.dataB)
        self.assertAlmostEqual(kappaVal, -0.23076923076923078)
        return

    def testZeroKappa(self):
        kappaVal = kappa(self.dataA, [0,0,6,6])
        self.assertAlmostEqual(kappaVal, 0)
        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

class CombinationTest(unittest.TestCase):
    def setUp(self):
        self.dataA = [1,2,3]

    def testCombinations(self):
        self.assertEqual(combinations([self.dataA, self.dataA]),
                [(1,1),(2,1),(3,1),(1,2),(2,2),(3,2),(1,3),(2,3),(3,3)])
        return

    def testICombinations(self):
        self.assertEqual(list(icombinations([self.dataA, self.dataA])),
                [(1,1),(2,1),(3,1),(1,2),(2,2),(3,2),(1,3),(2,3),(3,3)])

        return

    def testUniqueTuples(self):
        self.assertEqual(uniqueTuples([1,2]), [(1,2)])
        self.assertEqual(uniqueTuples([1,2,3]), [(1,2), (1,3), (2,3)])

        return

    def testInclusionCombination(self):
        self.assertEqual(
                set(map(tuple, inclusionCombinations([1,2]))),
                set(map(tuple, [[], [1], [2], [1,2]])),
            )
        self.assertEqual(inclusionCombinations([]), [[]])
        return

    def testIUniqueTuples(self):
        self.assertEqual(list(iuniqueTuples([1,2])), [(1,2)])
        self.assertEqual(list(iuniqueTuples([1,2,3])), [(1,2), (1,3), (2,3)])

        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
