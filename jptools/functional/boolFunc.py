# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# boolFunc.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 15:50:00 2007
#
#----------------------------------------------------------------------------#

"""
Functions that work on boolean methods, and high-level shortcuts for dealing
with booleans.
"""

#----------------------------------------------------------------------------#

from itertools import izip, chain

#----------------------------------------------------------------------------#

def addFunc(a, b):
    """
    Returns a + b::

        >>> addFunc(1, 3.0)
        4.0
    """
    return a + b

#----------------------------------------------------------------------------#

def timesFunc(a, b):
    """
    Returns a * b::

        >>> timesFunc(2, -10.0)
        -20.0
    """
    return a * b;

#----------------------------------------------------------------------------#

def orFunc(a, b):
    """
    Returns the boolean result of a OR b::

        >>> orFunc([], u'dog')
        u'dog'

        >>> orFunc(False, False)
        False
    """
    return a or b

#----------------------------------------------------------------------------#

def andFunc(a, b):
    """
    Returns the boolean result of a AND b.

        >>> andFunc(1, 100)
        100

        >>> andFunc(bool(1), bool(100))
        True

        >>> andFunc(False, True)
        False
    """
    return a and b

#----------------------------------------------------------------------------#

def allTrue(boolList):
    u"""
    Returns True if every object in the list evaluates to True.

        >>> allTrue([True, True, True])
        True

        >>> allTrue([True, False, True])
        False
    """
    for item in boolList:
        if not item:
            return False
    else:
        return True

#----------------------------------------------------------------------------#

def someTrue(boolList):
    u"""
    Returns True if at least one item in the list evaluates to True.

        >>> someTrue([True, False])
        True
        
        >>> someTrue([False, False])
        False
    """
    for item in boolList:
        if item:
            return True
    else:
        return False

#----------------------------------------------------------------------------#
