# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testSmartCache.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Feb  1 17:21:24 EST 2006
#
#----------------------------------------------------------------------------#

"""
Tests for the smartCache module.
"""

#----------------------------------------------------------------------------#

import os, sys, unittest
import smartCache
import doctest

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(CacheTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class CacheTestCase(unittest.TestCase):
    def setUp(self):
        self.numCalls = 0

        self.depFile = 'tmpDepFile'
        self.cacheFile = 'tmpCacheFile'

        # make sure our depFile exists and is non-empty
        oStream = open(self.depFile, 'w')
        print >> oStream, 'Started file here!!!'
        oStream.close()

        return

    def factoryMethod1(self, x):
        """
        A simple factory method for testing.
        """
        self.numCalls += 1
        return x*3

    def testPairedCache(self):
        """
        Tests the combination of using tryCache() and storeCacheObject().
        """
        # we shouldn't be returning an object when none have been cached
        obj = smartCache.tryCache(self.cacheFile, dependencies=[self.depFile])
        self.assertEqual(obj, None)

        # create an object, and cache it
        obj = self.factoryMethod1(10)
        smartCache.storeCacheObject(obj, self.cacheFile)

        # load from cache; it should be the same as the old object
        newObj = smartCache.tryCache(self.cacheFile, 
                dependencies=[self.depFile])
        self.assertEqual(newObj, obj)

        # now touch the dependency, after a significant delay
        os.system('sleep 1')
        oStream = open(self.depFile, 'w')
        print >> oStream, "A new change has been made to this file"
        oStream.close()

        # refetch; it shouldn't be cached
        newObj = smartCache.tryCache(self.cacheFile, [self.depFile])
        self.assertEqual(newObj, None)

        return

    def testProxyMethod(self):
        """
        Simple tests for the proxy() method.
        """
        self.assertEqual(self.numCalls, 0)

        # first fetch should trigger the actual call
        proxyMethod = smartCache.diskProxyDirect(
                self.factoryMethod1,
                self.cacheFile,
                [self.depFile]
            )

        self.assertEqual(proxyMethod(2), 6)
        self.assertEqual(self.numCalls, 1)

        self.assertEqual(proxyMethod(2), 6)
        self.assertEqual(self.numCalls, 1)

        # changing a dependency, should trigger an additional call
        os.system('sleep 1')
        oStream = open(self.depFile, 'a')
        print >> oStream, "Added a line"
        oStream.close()

        self.assertEqual(proxyMethod(2), 6)
        self.assertEqual(self.numCalls, 2)

        return

    def tearDown(self):
        """
        Delete the files used if they are still around.
        """
        if os.path.exists(self.cacheFile):
            os.remove(self.cacheFile)

        if os.path.exists(self.depFile):
            os.remove(self.depFile)
            
        return

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.main()

