# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# smartCache.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Fri Sep  9 15:17:56 EST 2005
#
#----------------------------------------------------------------------------#

"""
This module implements a smart caching function, with dependencies.
"""

#----------------------------------------------------------------------------#

import common
import cPickle as pickle
import time
import types
from os import path, environ
import sys, os

#----------------------------------------------------------------------------#

def diskProxyDirect(method, cacheFile, dependencies=[]):
    """
    Creates a proxy for an expensive method which is cached in a single 
    file.

    @param method: The method whose return values to cache.
    @param cacheFile: Where to cache the return values.
    @param dependencies: Any files which are dependencies for the cache.
    @return: A callable object that looks just like method.
    """
    def proxyMethod(*args, **params):
        cachedVal = tryCache(cacheFile, args, params, dependencies)

        if cachedVal is None:
            if 'CACHE_DEBUG' in os.environ:
                print '[cache miss: %s]' % os.path.basename(cacheFile)
            # cache miss, expensive fetch and repopulate cache
            result = apply(method, args, params)
            if 'CACHE_DEBUG' in os.environ:
                print '[storing: %s]' % os.path.basename(cacheFile)
            storeCacheObject(result, cacheFile, args, params)
            return result
        else:
            if 'CACHE_DEBUG' in os.environ:
                print '[cache hit: %s]' % os.path.basename(cacheFile)
            # cache hit
            return cachedVal

    proxyMethod.__doc__ = method.__doc__

    return proxyMethod

#----------------------------------------------------------------------------#

def diskProxy(cacheFile, dependencies):
    """
    Decorator version of diskProxyDirect().
    """
    return lambda method: diskProxyDirect(method, cacheFile, dependencies)

#----------------------------------------------------------------------------#

def memoryProxy(method):
    """
    Creates an in-memory proxy for the given method. This method is
    suitable for use wrapping expensive methods with small return values.

    This proxy will demonstrate unbounded growth if you keep using the
    method on new input. The references kept here prevent the results and
    arguments from being garbage-collected. If that's not what you want,
    consider the weakref.proxy() method in the standard python library.
    """
    methodDict = {}

    def proxyMethod(*args, **params):
        key = (args, tuple(params.items()))
        if methodDict.has_key(key):
            # cache hit
            return methodDict[key]
        else:
            # cache miss, expensive call and insert
            result = apply(method, args, params)
            methodDict[key] = result
            return result

    proxyMethod.__doc__ = method.__doc__

    return proxyMethod

#----------------------------------------------------------------------------#

def tryCache(filename, methodArgs=[], methodParams={}, dependencies=[]):
    """
    Determines whether the cached object is still fresh (if one exists),
    and if so returns that object. Otherwise returns None.
    
    @param filename: The filename to look for a cached entry in.
    @param methodArgs: The arguments passed to the method we're trying to
        cache.
    @param methodParams: As for methodArgs, but dictionary arguments. 
    @return: None or a stored value
    """
    if needsUpdate(filename, dependencies):
        return None

    try:
        iStream = common.sopen(filename, 'r', encoding=None)
        storedArgs = pickle.load(iStream)
        storedParams = pickle.load(iStream)

        if storedArgs == methodArgs and storedParams == methodParams:
            obj = pickle.load(iStream)
            iStream.close()
            return obj
        else:
            iStream.close()
            return None
    except:
        # could get several errors here:
        # - badly pickled file
        # - changed local modules when loading pickled value
        # - filesystem permissions or problems
        return None

#----------------------------------------------------------------------------#

def storeCacheObject(obj, filename, methodArgs=[], methodParams={}):
    """
    Creates a smart cache object in the file.
    
    @param obj: The object to cache.
    @param filename: The location of the cache file.
    @param methodArgs: Any arguments which were passed to the cached
        method.
    @param methodParams: Any keyword parameters passed to the cached
        method. 
    """
    oStream = common.sopen(filename, 'w', encoding=None)
    pickle.dump(methodArgs, oStream, pickle.HIGHEST_PROTOCOL)
    pickle.dump(methodParams, oStream, pickle.HIGHEST_PROTOCOL)
    pickle.dump(obj, oStream, pickle.HIGHEST_PROTOCOL)
    oStream.close()
    
    return

#----------------------------------------------------------------------------#

def needsUpdate(target, dependencies):
    """
    Determine if the target is older than any of its dependencies.

    @param target: A filename for the target.
    @param dependencies: A sequence of dependency filenames.
    """
    if not path.exists(target):
        return True

    targetTime = path.getmtime(target)

    for dependency in dependencies:
        if type(dependency) in (str, unicode):
            filenames = [dependency]

        elif type(dependency) == types.ModuleType:
            filenames = _getModuleDependencies(dependency)

        else:
            raise TypeError, "Unknown dependency type %s" % (type(dependency))

        for filename in filenames:
            if path.getmtime(filename) > targetTime:
                return True
    else:
        return False

#----------------------------------------------------------------------------#
# PRIVATE
#----------------------------------------------------------------------------#

def _getModuleDependencies(module):
    """
    Determines the file dependencies of a module. Adds one level of module
    includes.
    """
    dependencySet = set()
    dependencySet.add(module.__file__)

    for item in module.__dict__.values():
        if type(item) == types.ModuleType and hasattr(item, '__file__'):
            dependencySet.add(item.__file__)

    return dependencySet

#----------------------------------------------------------------------------#
