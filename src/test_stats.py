# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_stats.py
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
    test_suite = unittest.TestSuite((
            unittest.makeSuite(KappaTest),
            unittest.makeSuite(CombinationTest),
            unittest.makeSuite(BasicStatsTest),
        ))
    return test_suite

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

    def test_mean(self):
        """
        Check that mean works as expected.
        """
        self.assertAlmostEqual(mean(self.dataA), self.meanA, 5)
        self.assertAlmostEqual(mean(self.dataB), self.meanB, 5)
        return

    def test_bins_by_data(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,7,3,0]

        expected_labels = [(0,3), (3,5), (5,7)]
        expected_bins = [[0,1,2], [3,3], [5,7]]

        self.assertEqual(
                list(bins_by_data(data, 3)),
                zip(expected_labels, expected_bins)
            )

        return

    def test_bins_by_range(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,9,3,0]

        expected_labels = [(0.0,3.0), (3.0,6.0), (6.0,9.0)]
        expected_bins = [[0,1,2], [3,3,5], [9]]

        self.assertEqual(
                list(bins_by_range(data, 3, lambda x: x)),
                zip(expected_labels, expected_bins)
            )

        return

    def test_bins_by_inc(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,8,3,0]

        expected_labels = [(0.0,3.0), (3.0,6.0), (6.0,9.0)]
        expected_bins = [[0,1,2], [3,3,5], [8]]

        self.assertEqual(
                list(bins_by_increment(data, 3.0, lambda x: x)),
                zip(expected_labels, expected_bins)
            )

        data = [3,2,5,1,9,3,0]

        expected_labels = [(0.0,3.0), (3.0,6.0), (6.0,9.0), (9.0, 12.0)]
        expected_bins = [[0,1,2], [3,3,5], [], [9]]

        self.assertEqual(
                list(bins_by_increment(data, 3.0, lambda x: x)),
                zip(expected_labels, expected_bins)
            )

        return

    def test_bad_stddev(self):
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

    def test_stddev(self):
        """
        Check that stddev works as expected.
        """
        self.assertAlmostEqual(stddev(self.dataA), self.stddevA, 5)
        self.assertAlmostEqual(stddev(self.dataB), self.stddevB, 5)
        return

    def test_on_tuples(self):
        """
        Checks that methods also work on tuples.
        """
        self.assertAlmostEqual(mean(tuple(self.dataA)), self.meanA, 5)
        self.assertAlmostEqual(mean(tuple(self.dataB)), self.meanB, 5)
        self.assertAlmostEqual(stddev(tuple(self.dataA)), self.stddevA, 5)
        self.assertAlmostEqual(stddev(tuple(self.dataB)), self.stddevB, 5)
        return

    def test_basic_stats(self):
        """
        Test that the basic stats method works.
        """
        meanA, stddevA = basic_stats(self.dataA)
        self.assertAlmostEqual(meanA, mean(self.dataA))
        self.assertAlmostEqual(stddevA, stddev(self.dataA))
        return

    def test_segment_combinations(self):
        result = set([('d', 'o', 'g'), ('do', 'g'), ('d', 'og'), ('dog',)])
        self.assertEqual(
                set(segment_combinations(['d', 'o', 'g'])),
                result
            )
        self.assertEqual(
                set(isegment_combinations(['d', 'o', 'g'])),
                result
            )

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

class KappaTest(unittest.TestCase):
    def setUp(self):
        self.dataA = [1, 2, 3, 4]
        self.dataB = [2, 3, 4, 5]

    def test_high_kappa(self):
        """
        Tests a high kappa value
        """
        kappa_val = kappa(self.dataA, self.dataA)
        self.assertAlmostEqual(kappa_val, 1.0)
        return
    
    def test_no_agreement(self):
        """
        Tests the no agreement case.
        """
        kappa_val = kappa(self.dataA, self.dataB)
        self.assertAlmostEqual(kappa_val, -0.23076923076923078)
        return

    def test_zero_kappa(self):
        kappa_val = kappa(self.dataA, [0,0,6,6])
        self.assertAlmostEqual(kappa_val, 0)
        return

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

class CombinationTest(unittest.TestCase):
    def setUp(self):
        self.dataA = [1,2,3]

    def test_combinations(self):
        self.assertEqual(combinations([self.dataA, self.dataA]),
                [(1,1),(2,1),(3,1),(1,2),(2,2),(3,2),(1,3),(2,3),(3,3)])
        return

    def test_i_combinations(self):
        self.assertEqual(list(icombinations([self.dataA, self.dataA])),
                [(1,1),(2,1),(3,1),(1,2),(2,2),(3,2),(1,3),(2,3),(3,3)])

        return

    def test_unique_tuples(self):
        self.assertEqual(unique_tuples([1,2]), [(1,2)])
        self.assertEqual(unique_tuples([1,2,3]), [(1,2), (1,3), (2,3)])

        return

    def test_inclusion_combination(self):
        self.assertEqual(
                set(map(tuple, inclusion_combinations([1,2]))),
                set(map(tuple, [[], [1], [2], [1,2]])),
            )
        self.assertEqual(inclusion_combinations([]), [[]])
        return

    def test_i_unique_tuples(self):
        self.assertEqual(list(iunique_tuples([1,2])), [(1,2)])
        self.assertEqual(list(iunique_tuples([1,2,3])), [(1,2), (1,3), (2,3)])

        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
