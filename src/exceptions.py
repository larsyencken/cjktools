# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# exceptions.py
# Lars Yencken <lars.yencken@gmail.com>
# vim: ts=4 sw=4 sts=4 et tw=78:
# Tue Dec 26 13:18:46 2006
#
#----------------------------------------------------------------------------#

"""
A series of useful, common exceptions.
"""

#----------------------------------------------------------------------------#

class AbstractMethodError(Exception):
    """
    Indicates that a base class has had its abstract method called.
    """
    pass

#----------------------------------------------------------------------------#

class NotYetImplementedError(Exception):
    """
    A placeholder to use when you define a method but haven't implemented
    it yet.
    """
    pass

#----------------------------------------------------------------------------#
