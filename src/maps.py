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

def chain_mapping(*dictionaries):
    """
    Say you have more than one dictionary, and the range of the first is
    the domain of the second. You can create a new dictionary with the
    domain of the first but range of the second using this method.

        >>> chain_mapping({1: 'dog'}, {'dog': 3.0})
        {1: 3.0}
    """
    base_dict = dictionaries[0].copy()

    for dictionary in dictionaries[1:]:
        map_dict(dictionary.__getitem__, base_dict, in_place=True)

    return base_dict

#----------------------------------------------------------------------------#

def invert_mapping(dictionary):
    """
    Inverts a dictionary with a one-to-many mapping from key to value to a
    new dictionary with a one-to-many mapping from value to key.
    """
    inverted_dict = {}
    for key, values in dictionary.iteritems():
        for value in values:
            inverted_dict.setdefault(value, []).append(key)

    return inverted_dict

#----------------------------------------------------------------------------#

def is_injective(dictionary):
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

def invert_injective_mapping(dictionary):
    """
    Inverts a dictionary with a one-to-one mapping from key to value, into a
    new dictionary with a one-to-one mapping from value to key.
    """
    inverted_dict = {}
    for key, value in dictionary.iteritems():
        assert not inverted_dict.has_key(value), "Mapping is not 1-1"
        inverted_dict[value] = key

    return inverted_dict

#----------------------------------------------------------------------------#

def map_dict(method, dictionary, in_place=False):
    """
    Applies the method to every value in the dictionary, ignoring keys. If the
    in_place keyword is True, the existing dictionary is modified and returned.

    @param method: The method to apply.
    @param dictionary: The dictionary whose values to apply the method to.
    @return: A dictionary with the updated values.
    """
    if in_place:
        # Modify the dictionary in-place.
        for key, value in dictionary.iteritems():
            dictionary[key] = method(value)
        return dictionary
    else:
        # Return the modified dictionary.
        return dict((k, method(v)) for (k, v) in dictionary.iteritems())

#----------------------------------------------------------------------------#

def multi_dict(input_pairs):
    """
    Similar to casting pairs to a dictionary, except that repeated pairs
    are allowed. To show the difference:
    
        >>> dict( [('a', 1), ('b', 2), ('a', 3)] )
        {'a': 3, 'b': 2}

        >>> multi_dict( [('a', 1), ('b', 2), ('a', 3)] )
        {'a': [1, 3], 'b': [2]}

    @param input_pairs: A list of (key, value) pairs.
    @return: A dictionary mapping keys to lists of values.
    """
    output_dict = {}

    for key, value in input_pairs:
        existing_values = output_dict.get(key, [])
        existing_values.append(value)
        output_dict[key] = existing_values
    
    return output_dict

#----------------------------------------------------------------------------#

def procmap(procedure, item_list):
    """
    Like map(), but where the method being applied has no return value. In
    other words, the procedure is called on every item in the list
    sequentially, but since each call has no return value, the call to
    procmap() also has no return value.

    @param procedure: The procedure to call each time.
    @param item_list: The list of items to apply the procedure to.
    @return: None
    """
    for item in item_list:
        method(item)
    
    return

#----------------------------------------------------------------------------#

def merge_dicts(*args):
    """
    Merges a number of dictionaries together into one. Assumes the dictionary
    maps to a set of hashable items. The result for each key is the union of
    all the values in the provided dictionaries.
    """
    unified_dict = {}
    for key, items in apply(chain, [d.iteritems() for d in args]):
        if unified_dict.has_key(key):
            unified_dict[key].update(items)
        else:
            unified_dict[key] = set(items)

    return unified_dict

#----------------------------------------------------------------------------#

def partial_map(method, object_seq):
    """
    Like map, but filters out all objects with an non-true result, and
    returns them in a separate items list. I.e. any item for which the map
    resulted in a non-true value is provided in a "reject" list.

    @param method: The method to perform on each item.
    @type method: function
    @param object_seq: The sequence of items to apply the method to.
    @type object_seq: sequence
    @return: The tuple of lists (mapped_items, rejected_items).
    """
    mapped = []
    rejected = []

    for item in object_seq:
        result = apply(method, (item,))
        if result:
            mapped.append(result)
        else:
            rejected.append(item)
    
    return mapped, rejected

#----------------------------------------------------------------------------#

def filtered_map(method, object_list):
    """
    Performs a map then a filter on the object list. The final filter strips
    out objects which evaluate to False.
    """
    return filter(None, map(method, object_list))

#----------------------------------------------------------------------------#

