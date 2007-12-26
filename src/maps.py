# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# maps.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 14:49:38 2007
#
#----------------------------------------------------------------------------#

"""
This module considers dictionaries as discrete functional mappings, and
contains high-level interfaces for dealing with these mappings. 
"""

#----------------------------------------------------------------------------#

from itertools import izip, chain

#----------------------------------------------------------------------------#

def chainMapping(*dictionaries):
    """
    Say you have more than one dictionary, and the range of the first is
    the domain of the second. You can create a new dictionary with the
    domain of the first but range of the second using this method.

        >>> chainMapping({1: 'dog'}, {'dog': 3.0})
        {1: 3.0}
    """
    baseDict = dictionaries[0].copy()

    for dictionary in dictionaries[1:]:
        mapDict(dictionary.__getitem__, baseDict, inPlace=True)

    return baseDict

#----------------------------------------------------------------------------#

def invertMapping(dictionary):
    """
    Inverts a dictionary with a one-to-many mapping from key to value to a
    new dictionary with a one-to-many mapping from value to key.
    """
    invertedDict = {}
    for key, values in dictionary.iteritems():
        for value in values:
            invertedDict.setdefault(value, []).append(key)

    return invertedDict

#----------------------------------------------------------------------------#

def isInjective(dictionary):
    """
    Returns True if the mapping is one-to-one, False otherwise.

    Mapping keys are naturally unique, so this method just verifies that the
    values are also unique. This requires that the values are all hashable.
    """
    covered = set()
    for key, value in dictionary.iteritems():
        if value in covered:
            return False
        covered.add(value)
    else:
        return True

#----------------------------------------------------------------------------#

def invertInjectiveMapping(dictionary):
    """
    Inverts a dictionary with a one-to-one mapping from key to value, into a
    new dictionary with a one-to-one mapping from value to key.
    """
    invertedDict = {}
    for key, value in dictionary.iteritems():
        assert not invertedDict.has_key(value), "Mapping is not 1-1"
        invertedDict[value] = key

    return invertedDict

#----------------------------------------------------------------------------#

def mapDict(method, dictionary, inPlace=False):
    """
    Applies the method to every value in the dictionary, ignoring keys. If the
    inPlace keyword is True, the existing dictionary is modified and returned.

    @param method: The method to apply.
    @param dictionary: The dictionary whose values to apply the method to.
    @return: A dictionary with the updated values.
    """
    if inPlace:
        # Modify the dictionary in-place.
        for key, value in dictionary.iteritems():
            dictionary[key] = method(value)
        return dictionary
    else:
        # Return the modified dictionary.
        return dict((k, method(v)) for (k, v) in dictionary.iteritems())

#----------------------------------------------------------------------------#

def multiDict(inputPairs):
    """
    Similar to casting pairs to a dictionary, except that repeated pairs
    are allowed. To show the difference:
    
        >>> dict( [('a', 1), ('b', 2), ('a', 3)] )
        {'a': 3, 'b': 2}

        >>> multiDict( [('a', 1), ('b', 2), ('a', 3)] )
        {'a': [1, 3], 'b': [2]}

    @param inputPairs: A list of (key, value) pairs.
    @return: A dictionary mapping keys to lists of values.
    """
    outputDict = {}

    for key, value in inputPairs:
        existingValues = outputDict.get(key, [])
        existingValues.append(value)
        outputDict[key] = existingValues
    
    return outputDict

#----------------------------------------------------------------------------#

def procmap(procedure, itemList):
    """
    Like map(), but where the method being applied has no return value. In
    other words, the procedure is called on every item in the list
    sequentially, but since each call has no return value, the call to
    procmap() also has no return value.

    @param procedure: The procedure to call each time.
    @param itemList: The list of items to apply the procedure to.
    @return: None
    """
    for item in itemList:
        method(item)
    
    return

#----------------------------------------------------------------------------#

def mergeDicts(*args):
    """
    Merges a number of dictionaries together into one. Assumes the dictionary
    maps to a set of hashable items. The result for each key is the union of
    all the values in the provided dictionaries.
    """
    unifiedDict = {}
    for key, items in apply(chain, [d.iteritems() for d in args]):
        if unifiedDict.has_key(key):
            unifiedDict[key].update(items)
        else:
            unifiedDict[key] = set(items)

    return unifiedDict

#----------------------------------------------------------------------------#

def partialMap(method, objectSeq):
    """
    Like map, but filters out all objects with an non-true result, and
    returns them in a separate items list. I.e. any item for which the map
    resulted in a non-true value is provided in a "reject" list.

    @param method: The method to perform on each item.
    @type method: function
    @param objectSeq: The sequence of items to apply the method to.
    @type objectSeq: sequence
    @return: The tuple of lists (mappedItems, rejectedItems).
    """
    mapped = []
    rejected = []

    for item in objectSeq:
        result = apply(method, (item,))
        if result:
            mapped.append(result)
        else:
            rejected.append(item)
    
    return mapped, rejected

#----------------------------------------------------------------------------#

def filteredMap(method, objectList):
    """
    Performs a map then a filter on the object list. The final filter strips
    out objects which evaluate to False.
    """
    return filter(None, map(method, objectList))

#----------------------------------------------------------------------------#

