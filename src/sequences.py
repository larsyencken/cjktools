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

def zipWith(method, listA, listB):
    """
    Applies a two-argument method to successive pairs of items taken from
    the two input lists. Returns the list of resulting items.

    @param method: The two-argument method to run over element pairs.
    @param listA: The first providing the first tuple element for each
        pair.
    @param listB: The first providing the second tuple element for each
        pair.
    """
    return list(izipWith(method, listA, listB))

#----------------------------------------------------------------------------#

def izipWith(method, listA, listB):
    """
    As with zipWith(), but provides an iterator. 
    """
    for itemA, itemB in izip(listA, listB):
        yield method(itemA, itemB)
    
    return

#----------------------------------------------------------------------------#

def flatten(objectSeq):
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
    return list(iflatten(objectSeq))

#----------------------------------------------------------------------------#

def iflatten(objectSeq):
    """
    Returns an iterator over all the objects in the flattened sequence. The
    original order is preserved.

    @param objectSeq: A sequence of objects which themselves may be sequences
    (and their children, etc.).
    @type objectSeq: sequence
    @return: An iterator over all items in all subsequences.
    """
    objectSeq = iter(objectSeq)

    while True:
        try:
            item = objectSeq.next()

            if type(item) in (unicode, str):
                yield item
                continue
            try:
                # Try to coerce this item into a sequence.
                subSeq = iter(item)
            except TypeError:
                # Failed, it's not a sequence of objects.
                yield item
            else:
                # Succeeded, it's a subsequence, so iterate into it.
                objectSeq = chain(iter(item), objectSeq)

        except StopIteration:
            break

    return

#----------------------------------------------------------------------------#

def unzip(pairList):
    """
    The reverse of the zip() method. Given a sequence of tuples of the
    same size, extracts two or more lists.

        >>> unzip([(1,2), (3,4), (5,6)])
        ([1, 3, 5], [2, 4, 6])

    @param pairList: The sequence of tuples to draw the input from.
    """
    if not pairList:
        raise ValueError, "need a non-empty input list"

    numLists = len(pairList[0])

    newLists = []
    for i in range(numLists):
        newLists.append([])

    for pair in pairList:
        for i in range(numLists):
            newLists[i].append(pair[i])
    
    return tuple(newLists)

#----------------------------------------------------------------------------#

def thread(inputList, tupleSize=2):
    """
    Turns a list of items into a list of tuples by simply placing
    sequential items into tuples:

        >>> thread([1, 2, 3, 4, 5])
        [(1, 2), (3, 4)]

    Notice that the last element might be discarded, in a similar manner
    as when using zip.
    """
    return list(ithread(inputList, tupleSize))

#----------------------------------------------------------------------------#

def ithread(inputSeq, tupleSize=2):
    """
    Identical to thread() but returns an interator over pairs.

        >>> list(ithread([1, 2, 3, 4, 5]))
        [(1, 2), (3, 4)]
    """
    inputSeq = iter(inputSeq)

    listRange = range(tupleSize)
    while True:
        output = []
        try:
            for i in range(tupleSize):
                output.append(inputSeq.next())
        except StopIteration:
            break

        else:
            yield tuple(output)

    return

#----------------------------------------------------------------------------#

def iunthread(inputTuples):
    """
    Turns a list of tuples into a flat list:

        >>> list(iunthread([(1, 2), (3, 4)]))
        [1, 2, 3, 4]

    @param inputTuples: A list of tuples
    @type inputTuples: list(tuple)
    @return: A flat list
    """
    for itemTuple in inputTuples:
        for item in itemTuple:
            yield item

    return

#----------------------------------------------------------------------------#

def unthread(inputTuples):
    """
    Turns a list of tuples into a flat list:

        >>> unthread([(1, 2), (3, 4)])
        [1, 2, 3, 4]

    @param inputTuples: A list of tuples
    @type inputTuples: list(tuple)
    @return: A flat list
    """
    return list(iunthread(inputTuples))

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

def repeateIndef(item):
    """Returns an iterator which repeats the item indefinitely."""
    while 1:
        yield item

    return

#----------------------------------------------------------------------------#

def succession(itemList):
    """
    Returns an iterator which builds up the item list point by point.
        
        >>> list(succession([1, 2, 3]))
        [[1], [1, 2], [1, 2, 3]]
    """
    for i in xrange(1, len(itemList)+1):
        yield itemList[:i]
    
    return

#----------------------------------------------------------------------------#

def iwindow(itemList, windowSize=2, preBlanks=False):
    """
    Returns a sliding window iterator over the given list.

        >>> window([1, 2, 3, 4, 5])
        [(1, 2), (2, 3), (3, 4), (4, 5)]
        >>> window([1, 2, 3, 4], 3)
        [(1, 2, 3), (2, 3, 4)]
        >>> window([1, 2, 3, 4], 3, preBlanks=True)
        [(None, None, 1), (None, 1, 2), (1, 2, 3), (2, 3, 4)]

    @param itemList: The list to iterate over.
    @param windowSize: The number of elements in each window frame.
    """
    if preBlanks:
        if windowSize < 2:
            raise ValueError, "Need a window size >= 2 to use pre-blanks"
        itemList = [None]*(windowSize-1) + itemList

    for endWindow in range(windowSize, len(itemList)+1):
        yield tuple(itemList[endWindow-windowSize:endWindow])

    return 

def window(itemList, windowSize=2, preBlanks=False):
    """Identical to iwindow(), but returns a list."""
    return list(iwindow(itemList, windowSize, preBlanks))

#----------------------------------------------------------------------------#

def groupByLambda(func, items):
    """Performs a grouping of the items by lambda value."""
    import warn
    warn.warn(u'groupByLambda() is deprecated')
    groups = {}
    for item in items:
        keyValue = func(item)

        itemList = groups.get(keyValue, [])
        itemList.append(item)
        groups[keyValue] = itemList
    
    return groups

#----------------------------------------------------------------------------#

def multiDict(inputPairs):
    """
    Similar to casting pairs to a dictionary, except that repeated pairs
    are allowed.
    
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

def tailEnumerate(sequence):
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
    @return: A (trueList, falseList) tuple.
    """
    trueList = []
    falseList = []

    for item in seq:
        if method(item):
            trueList.append(item)
        else:
            falseList.append(item)

    return (trueList, falseList)

#----------------------------------------------------------------------------#

def separateByClass(method, seq):
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

def groupsOfN(n, seq):
    """
    Returns an iterator which groups elements of the sequence n at a time.

    >>> x = groupsOfN(3, range(10))
    >>> list(x) == [[0, 1, 2], [3, 4, 5], [6, 7 ,8], [9]]
    True
    """
    if hasattr(seq, '__getslice__'):
        return groupsOfNSliced(n, seq)
    else:
        return groupsOfNIter(n, seq)

#----------------------------------------------------------------------------#

def groupsOfNIter(n, seq):
    """A version of groupsOfN which always uses iterators."""
    seq = iter(seq)
    result = head(n, seq)
    while result:
        yield result
        result = head(n, seq)

    return

#----------------------------------------------------------------------------#

def groupsOfNSliced(n, seq):
    """A version of groupsOfN which always uses slices."""
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
