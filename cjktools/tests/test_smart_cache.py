# -*- coding: utf-8 -*-
#
#  test_smart_cache.py
#  cjktools
#

"""
Tests for the smart_cache module.
"""

from __future__ import print_function

import os
import time
import unittest
from cjktools import smart_cache


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(CacheTestCase),
    ))
    return test_suite


class CacheTestCase(unittest.TestCase):
    def setUp(self):
        self.num_calls = 0

        self.dep_file = 'tmp_dep_file'
        self.cache_file = 'tmp_cache_file'

        # make sure our dep_file exists and is non-empty
        with open(self.dep_file, 'w') as o_stream:
            print('Started file here!!!', file=o_stream)

    def factory_method1(self, x):
        """
        A simple factory method for testing.
        """
        self.num_calls += 1
        return x * 3

    def test_paired_cache(self):
        """
        Tests the combination of using try_cache() and store_cache_object().
        """
        # we shouldn't be returning an object when none have been cached
        obj = smart_cache.try_cache(self.cache_file, dependencies=[
            self.dep_file])
        self.assertEqual(obj, None)

        # create an object, and cache it
        obj = self.factory_method1(10)
        smart_cache.store_cache_object(obj, self.cache_file)

        # load from cache; it should be the same as the old object
        new_obj = smart_cache.try_cache(self.cache_file,
                                        dependencies=[self.dep_file])
        self.assertEqual(new_obj, obj)

        # now touch the dependency, after a significant delay
        time.sleep(1)
        with open(self.dep_file, 'w') as o_stream:
            print("A new change has been made to this file", file=o_stream)

        # refetch; it shouldn't be cached
        new_obj = smart_cache.try_cache(self.cache_file, [self.dep_file])
        self.assertEqual(new_obj, None)

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
        time.sleep(1)
        with open(self.dep_file, 'a') as o_stream:
            print(o_stream, "Added a line", file=o_stream)

        self.assertEqual(proxy_method(2), 6)
        self.assertEqual(self.num_calls, 2)

    def tearDown(self):
        """
        Delete the files used if they are still around.
        """
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)

        if os.path.exists(self.dep_file):
            os.remove(self.dep_file)


if __name__ == "__main__":
    unittest.main()
