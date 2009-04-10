# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_sequences.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 15:14:02 2007
#
#----------------------------------------------------------------------------#

import unittest
import doctest
import sequences

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(MiscTestCases),
            unittest.makeSuite(ThreadingTestCase),
            unittest.makeSuite(ZipWithTestCase),
        ))
    return test_suite

#----------------------------------------------------------------------------#

class MiscTestCases(unittest.TestCase):
    def test_separate(self):
        """
        Basic use of separate()
        """
        def is_even(i):
            return i % 2 == 0

        init_list = range(10)
        even, odd = sequences.separate(is_even, init_list)
        
        assert even == [0,2,4,6,8]
        assert odd == [1,3,5,7,9]

        return

    def test_flatten(self):
        data = [[1,2],3,[[4,[5,[]]]],[], set([1,2,3])]
        self.assertEqual(sequences.flatten(data), [1,2,3,4,5,1,2,3])
        self.assertEqual(list(sequences.iflatten(data)), [1,2,3,4,5,1,2,3])
        return

    def test_unzip(self):
        """
        Tests the unzip method.
        """
        data = zip(range(0, 5), range(4,9))
        unzipped_data = sequences.unzip(data)
        self.assertEqual(unzipped_data[0], range(0,5))
        self.assertEqual(unzipped_data[1], range(4,9))

        return

#----------------------------------------------------------------------------#

class ThreadingTestCase(unittest.TestCase):
    def test_thread(self):
        """
        Tests the variety of thread/unthread methods.
        """
        input_pairs = range(6)
        threaded_pairs = sequences.thread(input_pairs)
        self.assertEqual(threaded_pairs, [(0,1), (2,3), (4,5)])
        self.assertEqual(sequences.unthread(threaded_pairs), input_pairs)
        return

#----------------------------------------------------------------------------#

class ZipWithTestCase(unittest.TestCase):
    def test_basic(self):
        """
        Tests basic functioning of the zip_with method.
        """
        inputA = [1,-5, 0]
        inputB = [2, 5, 1]
        method = lambda x, y: x+y

        self.assertEqual(sequences.zip_with(method, inputA, inputB), [3, 0, 1])
        self.assertEqual(
                list(sequences.izip_with(method, inputA, inputB)),
                [3, 0, 1]
            )
        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#
