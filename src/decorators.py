# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# decorators.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Mar 27 13:51:56 2007
#
#----------------------------------------------------------------------------#

"""
A series of useful Python decorators.
"""

#----------------------------------------------------------------------------#

def simple_decorator(decorator):
    """Turns simple functions into well behaved decorators."""
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g

    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator

#----------------------------------------------------------------------------#

class memoized(object): 
    """A decorator which caches the functions values in a dictionary."""
    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args, **kwargs):
        kwargs_key = tuple(kwargs.items())
        try:
            return self.cache[(args, kwargs_key)]

        except KeyError:
            value = self.func(*args, **kwargs)
            self.cache[(args, kwargs_key)] = value
            return value

        except TypeError:
            # Uncacheable, for example if an argument is unhashable.
            return self.func(*args, **kwargs)

    def __repr__(self):
        return repr(self.func)

#----------------------------------------------------------------------------#

@simple_decorator
def one_shot(f):
    """Caches all calls to the function after the first."""
    def wrapper():
        if not hasattr(f, '_cached'):
            f._cached = f()

        return f._cached

    return wrapper

#----------------------------------------------------------------------------#

