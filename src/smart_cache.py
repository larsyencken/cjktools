# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# smart_cache.py
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

def disk_proxy_direct(method, cache_file, dependencies=[]):
    """
    Creates a proxy for an expensive method which is cached in a single 
    file.

    @param method: The method whose return values to cache.
    @param cache_file: Where to cache the return values.
    @param dependencies: Any files which are dependencies for the cache.
    @return: A callable object that looks just like method.
    """
    def proxy_method(*args, **params):
        cached_val = try_cache(cache_file, args, params, dependencies)

        if cached_val is None:
            if 'CACHE_DEBUG' in os.environ:
                print '[cache miss: %s]' % os.path.basename(cache_file)
            # cache miss, expensive fetch and repopulate cache
            result = apply(method, args, params)
            if 'CACHE_DEBUG' in os.environ:
                print '[storing: %s]' % os.path.basename(cache_file)
            store_cache_object(result, cache_file, args, params)
            return result
        else:
            if 'CACHE_DEBUG' in os.environ:
                print '[cache hit: %s]' % os.path.basename(cache_file)
            # cache hit
            return cached_val

    proxy_method.__doc__ = method.__doc__

    return proxy_method

#----------------------------------------------------------------------------#

def disk_proxy(cache_file, dependencies):
    """
    Decorator version of disk_proxy_direct().
    """
    return lambda method: disk_proxy_direct(method, cache_file, dependencies)

#----------------------------------------------------------------------------#

def memory_proxy(method):
    """
    Creates an in-memory proxy for the given method. This method is
    suitable for use wrapping expensive methods with small return values.

    This proxy will demonstrate unbounded growth if you keep using the
    method on new input. The references kept here prevent the results and
    arguments from being garbage-collected. If that's not what you want,
    consider the weakref.proxy() method in the standard python library.
    """
    method_dict = {}

    def proxy_method(*args, **params):
        key = (args, tuple(params.items()))
        if method_dict.has_key(key):
            # cache hit
            return method_dict[key]
        else:
            # cache miss, expensive call and insert
            result = apply(method, args, params)
            method_dict[key] = result
            return result

    proxy_method.__doc__ = method.__doc__

    return proxy_method

#----------------------------------------------------------------------------#

def try_cache(filename, method_args=[], method_params={}, dependencies=[]):
    """
    Determines whether the cached object is still fresh (if one exists),
    and if so returns that object. Otherwise returns None.
    
    @param filename: The filename to look for a cached entry in.
    @param method_args: The arguments passed to the method we're trying to
        cache.
    @param method_params: As for method_args, but dictionary arguments. 
    @return: None or a stored value
    """
    if needs_update(filename, dependencies):
        return None

    try:
        i_stream = common.sopen(filename, 'r', encoding=None)
        stored_args = pickle.load(i_stream)
        stored_params = pickle.load(i_stream)

        if stored_args == method_args and stored_params == method_params:
            obj = pickle.load(i_stream)
            i_stream.close()
            return obj
        else:
            i_stream.close()
            return None
    except:
        # could get several errors here:
        # - badly pickled file
        # - changed local modules when loading pickled value
        # - filesystem permissions or problems
        return None

#----------------------------------------------------------------------------#

def store_cache_object(obj, filename, method_args=[], method_params={}):
    """
    Creates a smart cache object in the file.
    
    @param obj: The object to cache.
    @param filename: The location of the cache file.
    @param method_args: Any arguments which were passed to the cached
        method.
    @param method_params: Any keyword parameters passed to the cached
        method. 
    """
    o_stream = common.sopen(filename, 'w', encoding=None)
    pickle.dump(method_args, o_stream, pickle.HIGHEST_PROTOCOL)
    pickle.dump(method_params, o_stream, pickle.HIGHEST_PROTOCOL)
    pickle.dump(obj, o_stream, pickle.HIGHEST_PROTOCOL)
    o_stream.close()
    
    return

#----------------------------------------------------------------------------#

def needs_update(target, dependencies):
    """
    Determine if the target is older than any of its dependencies.

    @param target: A filename for the target.
    @param dependencies: A sequence of dependency filenames.
    """
    if not path.exists(target):
        return True

    target_time = path.getmtime(target)

    for dependency in dependencies:
        if type(dependency) in (str, unicode):
            filenames = [dependency]

        elif type(dependency) == types.ModuleType:
            filenames = _get_module_dependencies(dependency)

        else:
            raise TypeError, "Unknown dependency type %s" % (type(dependency))

        for filename in filenames:
            if path.getmtime(filename) > target_time:
                return True
    else:
        return False

#----------------------------------------------------------------------------#
# PRIVATE
#----------------------------------------------------------------------------#

def _get_module_dependencies(module):
    """
    Determines the file dependencies of a module. Adds one level of module
    includes.
    """
    dependency_set = set()
    dependency_set.add(module.__file__)

    for item in module.__dict__.values():
        if type(item) == types.ModuleType and hasattr(item, '__file__'):
            dependency_set.add(item.__file__)

    return dependency_set

#----------------------------------------------------------------------------#
