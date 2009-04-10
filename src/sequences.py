# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# sequences.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Jun 25 14:53:16 2007
#
#----------------------------------------------------------------------------#

"""
This module contains methods for dealing with sequences. In particular, it
contains iterators for interesting sequences and methods for sequence/tuple
transformations.
"""

#----------------------------------------------------------------------------#

from itertools import izip, chain

#----------------------------------------------------------------------------#

def zip_with(method, listA, listB):
    """
    Applies a two-argument method to successive pairs of items taken from
    the two input lists. Returns the list of resulting items.

    @param method: The two-argument method to run over element pairs.
    @param listA: The first providing the first tuple element for each
        pair.
    @param listB: The first providing the second tuple element for each
        pair.
    """
    return list(izip_with(method, listA, listB))

#----------------------------------------------------------------------------#

def izip_with(method, listA, listB):
    """
    As with zip_with(), but provides an iterator. 
    """
    for itemA, itemB in izip(listA, listB):
        yield method(itemA, itemB)
    
    return

#----------------------------------------------------------------------------#

def flatten(object_seq):
    """
    Flattens all levels of lists from the input, preserving original order
    of items.

    >>> flatten([1, [2, [3, [], [4, 5, [6]]]]])
    [1, 2, 3, 4, 5, 6]
    >>> flatten([1, set(['a'])])
    [1, 'a']
    >>> flatten([1, set([u'a'])])
    [1, u'a']
    """
    return list(iflatten(object_seq))

#----------------------------------------------------------------------------#

def iflatten(object_seq):
    """
    Returns an iterator over all the objects in the flattened sequence. The
    original order is preserved.

    @param object_seq: A sequence of objects which themselves may be sequences
    (and their children, etc.).
    @type object_seq: sequence
    @return: An iterator over all items in all subsequences.
    """
    object_seq = iter(object_seq)

    while True:
        try:
            item = object_seq.next()

            if type(item) in (unicode, str):
                yield item
                continue
            try:
                # Try to coerce this item into a sequence.
                sub_seq = iter(item)
            except TypeError:
                # Failed, it's not a sequence of objects.
                yield item
            else:
                # Succeeded, it's a subsequence, so iterate into it.
                object_seq = chain(iter(item), object_seq)

        except StopIteration:
            break

    return

#----------------------------------------------------------------------------#

def unzip(pair_list):
    """
    The reverse of the zip() method. Given a sequence of tuples of the
    same size, extracts two or more lists.

        >>> unzip([(1,2), (3,4), (5,6)])
        ([1, 3, 5], [2, 4, 6])

    @param pair_list: The sequence of tuples to draw the input from.
    """
    if not pair_list:
        raise ValueError, "need a non-empty input list"

    num_lists = len(pair_list[0])

    new_lists = []
    for i in range(num_lists):
        new_lists.append([])

    for pair in pair_list:
        for i in range(num_lists):
            new_lists[i].append(pair[i])
    
    return tuple(new_lists)

#----------------------------------------------------------------------------#

def thread(input_list, tuple_size=2):
    """
    Turns a list of items into a list of tuples by simply placing
    sequential items into tuples:

        >>> thread([1, 2, 3, 4, 5])
        [(1, 2), (3, 4)]

    Notice that the last element might be discarded, in a similar manner
    as when using zip.
    """
    return list(ithread(input_list, tuple_size))

#----------------------------------------------------------------------------#

def ithread(input_seq, tuple_size=2):
    """
    Identical to thread() but returns an interator over pairs.

        >>> list(ithread([1, 2, 3, 4, 5]))
        [(1, 2), (3, 4)]
    """
    input_seq = iter(input_seq)

    list_range = range(tuple_size)
    while True:
        output = []
        try:
            for i in range(tuple_size):
                output.append(input_seq.next())
        except StopIteration:
            break

        else:
            yield tuple(output)

    return

#----------------------------------------------------------------------------#

def iunthread(input_tuples):
    """
    Turns a list of tuples into a flat list:

        >>> list(iunthread([(1, 2), (3, 4)]))
        [1, 2, 3, 4]

    @param input_tuples: A list of tuples
    @type input_tuples: list(tuple)
    @return: A flat list
    """
    for item_tuple in input_tuples:
        for item in item_tuple:
            yield item

    return

#----------------------------------------------------------------------------#

def unthread(input_tuples):
    """
    Turns a list of tuples into a flat list:

        >>> unthread([(1, 2), (3, 4)])
        [1, 2, 3, 4]

    @param input_tuples: A list of tuples
    @type input_tuples: list(tuple)
    @return: A flat list
    """
    return list(iunthread(input_tuples))

#----------------------------------------------------------------------------#

def repeat(n, item):
    """
    Creates an iterator which provides n references to item. Note that they
    are references, not copies.

        >>> list(repeat(10, 1)) == [1]*10
        True

    @param n: The number of copies to yield in total.
    @type n: int
    @param item: The item to repeat.
    @type item: object
    """
    for i in xrange(n):
        yield item
    return

#----------------------------------------------------------------------------#

def repeate_indef(item):
    """Returns an iterator which repeats the item indefinitely."""
    while 1:
        yield item

    return

#----------------------------------------------------------------------------#

def succession(item_list):
    """
    Returns an iterator which builds up the item list point by point.
        
        >>> list(succession([1, 2, 3]))
        [[1], [1, 2], [1, 2, 3]]
    """
    for i in xrange(1, len(item_list)+1):
        yield item_list[:i]
    
    return

#----------------------------------------------------------------------------#

def iwindow(item_list, window_size=2, pre_blanks=False):
    """
    Returns a sliding window iterator over the given list.

        >>> window([1, 2, 3, 4, 5])
        [(1, 2), (2, 3), (3, 4), (4, 5)]
        >>> window([1, 2, 3, 4], 3)
        [(1, 2, 3), (2, 3, 4)]
        >>> window([1, 2, 3, 4], 3, pre_blanks=True)
        [(None, None, 1), (None, 1, 2), (1, 2, 3), (2, 3, 4)]

    @param item_list: The list to iterate over.
    @param window_size: The number of elements in each window frame.
    """
    if pre_blanks:
        if window_size < 2:
            raise ValueError, "Need a window size >= 2 to use pre-blanks"
        item_list = [None]*(window_size-1) + item_list

    for end_window in range(window_size, len(item_list)+1):
        yield tuple(item_list[end_window-window_size:end_window])

    return 

def window(item_list, window_size=2, pre_blanks=False):
    """Identical to iwindow(), but returns a list."""
    return list(iwindow(item_list, window_size, pre_blanks))

#----------------------------------------------------------------------------#

def group_by_lambda(func, items):
    """Performs a grouping of the items by lambda value."""
    import warn
    warn.warn(u'group_by_lambda() is deprecated')
    groups = {}
    for item in items:
        key_value = func(item)

        item_list = groups.get(key_value, [])
        item_list.append(item)
        groups[key_value] = item_list
    
    return groups

#----------------------------------------------------------------------------#

def multi_dict(input_pairs):
    """
    Similar to casting pairs to a dictionary, except that repeated pairs
    are allowed.
    
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

def tail_enumerate(sequence):
    """
    Same as enumerate(), but yields tuples of (item, index), so that you can
    sort and otherwise use them nicely.
    """
    i = 0
    for item in sequence:
        yield (item, i)
        i += 1

    return

#----------------------------------------------------------------------------#

def separate(method, seq):
    """
    Uses the given method to separate the sequence into two lists, one for
    which method(item) returns True for every item, the other for which
    method(item) return False.

    @param method: The boolean-valued function to separate with.
    @type method: function
    @param seq: A sequence of objects.
    @type seq: sequence 
    @return: A (true_list, false_list) tuple.
    """
    true_list = []
    false_list = []

    for item in seq:
        if method(item):
            true_list.append(item)
        else:
            false_list.append(item)

    return (true_list, false_list)

#----------------------------------------------------------------------------#

def separate_by_class(method, seq):
    """
    Distributes a sequence into a dictionary of classes, using the given
    method's return value as the class label. This is a generalization of 
    the separate() method.

    @param method: The function generating class labels from items. 
    @type method: function
    @param seq: A sequence of objects.
    @type seq: sequence
    @return: A dictionary of class object lists.
    """
    results = {}
    for item in seq:
        key = method(item)
        if key in results:
            results[key].append(item)
        else:
            results[key] = [item]

    return results

#----------------------------------------------------------------------------#

def head(n, seq):
    """
    Returns an iterator over the first n items in a sequence.
    
    If the sequence is itself an iterator, this will also advance the
    iterator n places.

        >>> head(3, range(10))
        [0, 1, 2]

        >>> x = iter(xrange(10))
        >>> head(3, x)
        [0, 1, 2]
        >>> head(4, x)
        [3, 4, 5, 6]
        >>> head(100, x)
        [7, 8, 9]
    """
    if hasattr(seq, '__getslice__'):
        return seq[:n]

    result = []
    i = 0

    # The empty case.
    if n < 1:
        return

    for item in seq:
        result.append(item)

        i += 1
        if i >= n:
            break

    return result

#----------------------------------------------------------------------------#

def groups_of_n(n, seq):
    """
    Returns an iterator which groups elements of the sequence n at a time.

    >>> x = groups_of_n(3, range(10))
    >>> list(x) == [[0, 1, 2], [3, 4, 5], [6, 7 ,8], [9]]
    True
    """
    if hasattr(seq, '__getslice__'):
        return groups_of_n_sliced(n, seq)
    else:
        return groups_of_n_iter(n, seq)

#----------------------------------------------------------------------------#

def groups_of_n_iter(n, seq):
    """A version of groups_of_n which always uses iterators."""
    seq = iter(seq)
    result = head(n, seq)
    while result:
        yield result
        result = head(n, seq)

    return

#----------------------------------------------------------------------------#

def groups_of_n_sliced(n, seq):
    """A version of groups_of_n which always uses slices."""
    i = 0
    result = seq[i:i+n]
    while result:
        yield result
        i += n
        result = seq[i:i+n]
    return

#----------------------------------------------------------------------------#

def ihead(n, seq):
    """
    Returns an iterator over the first n items in a sequence.
    
    If the sequence is itself an iterator, this will also advance the
    iterator n places.

        >>> list(ihead(3, xrange(10)))
        [0, 1, 2]

        >>> x = iter(xrange(10))
        >>> list(ihead(3, x))
        [0, 1, 2]
        >>> list(ihead(4, x))
        [3, 4, 5, 6]
        >>> list(ihead(100, x))
        [7, 8, 9]
    """
    i = 0

    # The empty case.
    if n < 1:
        return

    for item in seq:
        yield item

        i += 1
        if i >= n:
            break

    return
#----------------------------------------------------------------------------#

def tail(n, seq):
    """
    Returns a list of the last n items in the iterator.

    This is particularly efficient if n is much smaller than the length of the
    iterator. It also requires O(n) storage.

        >>> tail(3, xrange(10))
        [7, 8, 9]

        >>> tail(10, xrange(3))
        [0, 1, 2]
    """
    output = n * [None]
    i = 0

    for item in seq:
        output[i % n] = item
        i += 1

    if i <= n:
        return output[:i]
    else:
        start = i % n
        return output[start:] + output[:start]

#----------------------------------------------------------------------------#
