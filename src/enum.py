# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# enum.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Wed Jul  6 16:39:53 EST 2005
#
#----------------------------------------------------------------------------#

"""
C style enums, with nice error checking such as only allowing comparisons
between elements of the same enum class.
"""

#----------------------------------------------------------------------------#

class Enum:
    def __init__(self, *names):
        constants = []
        for i, name in enumerate(names):
            val = EnumValue(i, name, self)
            constants.append(val)
            setattr(self, name, val)
        self._constants = tuple(constants)
        self._names = names

        return

    def __len__(self):
        return len(self._constants)

    def from_string(self, name):
        for constant in self._constants:
            if constant._name == name:
                return constant
        else:
            raise Exception, 'No such item in this enum'

    def __getitem__(self, i):
        return self._constants[i]

    def __repr__(self):
        return 'Enum' + str(self._names)

    def __str__(self):
        return 'enum' + str(self._constants)

#----------------------------------------------------------------------------#

class EnumValue:
    def __init__(self, value, name, parent):
        self._value = value
        self._parent = parent
        self._name = name
        return
    
    def __cmp__(self, other):
        assert type(other) == type(self), \
                "Only values from the same enum are comparable"
        return cmp(self._value, other._value)

    def __hash__(self):
        return hash(self._value)

    def __nonzero__(self):
        return bool(self._value)

    def __repr__(self):
        return str(self._name)

#----------------------------------------------------------------------------#
