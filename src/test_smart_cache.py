# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_smart_cache.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Feb  1 17:21:24 EST 2006
#
#----------------------------------------------------------------------------#

"""
Tests for the smart_cache module.
"""

#----------------------------------------------------------------------------#

import os, sys, unittest
import smart_cache
import doctest

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(CacheTestCase),
        ))
    return test_suite

#----------------------------------------------------------------------------#

class CacheTestCase(unittest.TestCase):
    def setUp(self):
        self.num_calls = 0

        self.dep_file = 'tmp_dep_file'
        self.cache_file = 'tmp_cache_file'

        # make sure our dep_file exists and is non-empty
        o_stream = open(self.dep_file, 'w')
        print >> o_stream, 'Started file here!!!'
        o_stream.close()

        return

    def factory_method1(self, x):
        """
        A simple factory method for testing.
        """
        self.num_calls += 1
        return x*3

    def test_paired_cache(self):
        """
        Tests the combination of using try_cache() and store_cache_object().
        """
        # we shouldn't be returning an object when none have been cached
        obj = smart_cache.try_cache(self.cache_file, dependencies=[self.dep_file])
        self.assertEqual(obj, None)

        # create an object, and cache it
        obj = self.factory_method1(10)
        smart_cache.store_cache_object(obj, self.cache_file)

        # load from cache; it should be the same as the old object
        new_obj = smart_cache.try_cache(self.cache_file, 
                dependencies=[self.dep_file])
        self.assertEqual(new_obj, obj)

        # now touch the dependency, after a significant delay
        os.system('sleep 1')
        o_stream = open(self.dep_file, 'w')
        print >> o_stream, "A new change has been made to this file"
        o_stream.close()

        # refetch; it shouldn't be cached
        new_obj = smart_cache.try_cache(self.cache_file, [self.dep_file])
        self.assertEqual(new_obj, None)

        return

    def test_proxy_method(self):
        """
        Simple tests for the proxy() method.
        """
        self.assertEqual(self.num_calls, 0)

        # first fetch should trigger the actual call
        proxy_method = smart_cache.disk_proxy_direct(
                self.factory_method1,
                self.cache_file,
                [self.dep_file]
            )

        self.assertEqual(proxy_method(2), 6)
        self.assertEqual(self.num_calls, 1)

        self.assertEqual(proxy_method(2), 6)
        self.assertEqual(self.num_calls, 1)

        # changing a dependency, should trigger an additional call
        os.system('sleep 1')
        o_stream = open(self.dep_file, 'a')
        print >> o_stream, "Added a line"
        o_stream.close()

        self.assertEqual(proxy_method(2), 6)
        self.assertEqual(self.num_calls, 2)

        return

    def tearDown(self):
        """
        Delete the files used if they are still around.
        """
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

        if os.path.exists(self.dep_file):
            os.remove(self.dep_file)
            
        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.main()

