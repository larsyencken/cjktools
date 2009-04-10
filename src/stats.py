# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# stats.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon May 16 14:18:59 EST 2005
#
#----------------------------------------------------------------------------#

"""
This module is responsible for any general combinatoric methods, in
particular determining possible combinations of input.
"""

#----------------------------------------------------------------------------#

from itertools import izip, ifilter
from math import sqrt

import warnings
warnings.warn(
        'please use simplestats package instead',
        DeprecationWarning,
    )

#----------------------------------------------------------------------------#

_eps = 1e-8

#----------------------------------------------------------------------------#

class InsufficientData(Exception):
    pass

#----------------------------------------------------------------------------#
# PUBLIC METHODS
#----------------------------------------------------------------------------#

def bins_by_data(data, n):
    """
    Puts the data into n sorted bins. Where n does not divide the length
    of the data directly, distributes the remainder as evenly as possible.
    Returns an iterator over the bins.

    @param data: A sequence of data. 
    """
    data.sort()

    assert n <= len(data), "Can't split a group more ways than its length"

    items_per_group, remainder = divmod(len(data), n)

    start_at = 0
    for i in xrange(n):
        end_at = start_at + items_per_group

        if remainder > 0:
            end_at += 1
            remainder -= 1

        yield (start_at, end_at), data[start_at:end_at]

        start_at = end_at

    return

#----------------------------------------------------------------------------#

def bins_by_increment(data, inc, key_method=lambda x: x[0]):
    """
    Calculates bins by range increment. Assumes data is a sequence of
    tuples, where the first tuple is the one whose range is divided up.
    """
    data = list(data)
    data.sort()

    # add _eps to the end of the range to ensure we capture that object
    start_range = key_method(data[0])
    end_range = key_method(data[-1]) + _eps

    for bin_start in frange(start_range, end_range, inc):
        bin_end = bin_start + inc

        bin_data = [x for x in data if key_method(x) >= bin_start and \
                key_method(x) < bin_end]

        yield (bin_start, bin_end), bin_data

    return

#----------------------------------------------------------------------------#

def bins_by_range(data, n, key_method=lambda x: x[0]):
    """
    Calculates bins by range. Assumes data is a sequence of tuples, where
    the first tuple is the one whose range is divided up.
    """
    data = list(data)
    data.sort()

    start_range = key_method(data[0])
    end_range = key_method(data[-1])
    bin_size = (end_range - start_range)/float(n)

    for i in xrange(n):
        bin_start = start_range + i*bin_size
        bin_end = start_range + (i+1)*bin_size

        # add eps to the size of the last bin to ensure we capture that
        # object
        if i == (n-1):
            use_bin_end = bin_end + _eps
        else:
            use_bin_end = bin_end

        bin_data = [x for x in data if key_method(x) >= bin_start and \
                key_method(x) < use_bin_end]

        yield (bin_start, bin_end), bin_data

    return

#----------------------------------------------------------------------------#

def combinations(combination_list):
    """
    Generates a list of all possible combinations of one element from the
    first item in combination_list, one from the second, etc. For example::

        >>> combinations([[1, 2], ['dog'], ['a', 'b']])
        [(1, 'dog', 'a'), (2, 'dog', 'a'), (1, 'dog', 'b'), (2, 'dog', 'b')]
    """
    combination_list = list(combination_list[:])
    combination_list.reverse()

    first_list = combination_list.pop()
    combos = map(lambda x: (x,), first_list)

    while combination_list:
        next_level_combos = []
        for item_to_add in combination_list.pop():
            # add this item to the end of every existing combo 
            for existing_combo in combos:
                next_level_combos.append(existing_combo + (item_to_add,))

        combos = next_level_combos

    return combos

#----------------------------------------------------------------------------#

def iunique_pairs(input_list):
    return UniquePairsIterator(input_list)

class UniquePairsIterator(object):
    """
    An interator over pairings which also has a length method.

    >>> x = UniquePairsIterator([1, 2, 3])
    >>> len(x)
    3
    >>> list(x)
    [(1, 2), (1, 3), (2, 3)]
    """
    def __init__(self, input_list):
        self.i = 0
        self.j = 1
        self.input_list = sorted(input_list)
        self.list_len = len(input_list)

        if self.list_len < 2:
            raise ValueError, "input must be of length at least 2"

    def next(self):
        if self.i == self.list_len - 1 and self.j >= self.list_len:
            raise StopIteration

        item = self.input_list[self.i], self.input_list[self.j]
        self.j += 1
        if self.j >= self.list_len:
            self.i += 1
            self.j = self.i + 1

        return item

    def __len__(self):
        return self.list_len * (self.list_len - 1) / 2

    def __iter__(self):
        return self

    def __repr__(self):
        return '<UniquePairsIterator: %d items>' % len(self)

#----------------------------------------------------------------------------#

def unique_tuples(input_list, n=2):
    "Similar to combinations, but selects from the same list."
    def filter_fn(x):
        for i in xrange(n-1):
            if x[i] >= x[i+1]:
                return False
        else:
            return True

    return filter(filter_fn, combinations(n*[input_list]))

#----------------------------------------------------------------------------#

def iunique_tuples(input_list, n=2):
    "An iterator version of unique_tuples."
    def filter_fn(x):
        for i in xrange(n-1):
            if x[i] >= x[i+1]:
                return False
        else:
            return True

    return ifilter(filter_fn, icombinations(n*[input_list]))

#----------------------------------------------------------------------------#

def icombinations(combination_lists):
    """
    As for combinations(), but returns an iterator.
    """
    combination_lists = map(list, combination_lists)
    lengths = map(len, combination_lists)
    combined = zip(combination_lists, lengths)
    n_combs = reduce(lambda x, y: x*y, lengths)

    for i in xrange(n_combs):
        item = ()
        for item_list, list_length in combined:
            i, offset = divmod(i, list_length)
            item += (item_list[offset],)
        yield item

    return

#----------------------------------------------------------------------------#

def combination_seqs(combination_list):
    """
    As with combinations() above, except that each potential item is
    assumed to already be in sequence form. For example::

        >>> combination_seqs([ [(1, 2), (3, 4)], [('dog',), ('cat',)] ])
        [(1, 2, 'dog'), (3, 4, 'dog'), (1, 2, 'cat'), (3, 4, 'cat')]
    """
    return list(icombination_seqs(combination_list))

#----------------------------------------------------------------------------#

def icombination_seqs(combination_lists):
    """
    As for combinations(), but returns an iterator.

        >>> list(icombination_seqs([ [(1, 2), (3, 4)], [('dog',), ('cat',)] ]))
        [(1, 2, 'dog'), (3, 4, 'dog'), (1, 2, 'cat'), (3, 4, 'cat')]
    """
    for seq_combs in icombinations(combination_lists):
        result = []
        for seq in seq_combs:
            result.extend(seq)
        yield tuple(result)
    return

#----------------------------------------------------------------------------#

def segment_combinations(g_string):    
    """
    Determines the possible segment combinations based on the grapheme
    string alone, in particular due to kanji placement. For example::

        >>> segment_combinations('ab')
        [('a', 'b'), ('ab',)]
    
    """
    # start out with just the first character
    segmentations = [[g_string[0]]]

    # add remaining characters one by one
    for char in g_string[1:]: 
        next_segmentation_round = []
        for segment in segmentations:
            # the new char in its own segment
            next_segmentation_round.append(segment + [char])

            # the new char as part of the previous segment
            segment[-1] += char
            next_segmentation_round.append(segment)

        segmentations = next_segmentation_round
    
    segmentations = map(tuple, segmentations)

    return segmentations

#----------------------------------------------------------------------------#

def isegment_combinations(g_string):
    """
    As for segment_combinations(), but returns an iterator.

        >>> list(sorted(isegment_combinations('ab')))
        [('a', 'b'), ('ab',)]

    Note that the order may be different.
    """
    if not g_string:
        return

    g_string_size = len(g_string)
    n_combs = 2**(g_string_size-1)

    for i in xrange(n_combs):
        current_comb = [g_string[0]]
        for j in xrange(1,g_string_size):
            i, has_boundary = divmod(i, 2)
            if has_boundary:
                current_comb.append(g_string[j])
            else:
                current_comb[-1] += g_string[j]
        yield tuple(current_comb)

    return

#----------------------------------------------------------------------------#

def kappa(responsesA, responsesB, potential_responses=None):
    """
    Assuming matched list of response values for each rater, determine
    their kappa value using Cohen's method.
    """
    from nltk.probability import FreqDist

    if not responsesA or not responsesB:
        raise InsufficientData, "Need at least one response to calculate kappa"

    if len(responsesA) != len(responsesB):
        raise ValueError, "Response vectors are different lengths"
    
    # Build rater bias distributions.
    biasA = FreqDist()
    for sample in responsesA:
        biasA.inc(sample)

    biasB = FreqDist()
    for sample in responsesB:
        biasB.inc(sample)

    if potential_responses is None:
        # Detect the sample range.
        potential_responses = set(biasA.samples()).union(biasB.samples())
    
    # calculate p_agreement: the actual frequency of agreement
    n_agreements = 0
    n_questions = 0
    for responseA, responseB in izip(responsesA, responsesB):
        if responseA == responseB:
            # they agreed 
            n_agreements += 1

        n_questions += 1

    assert n_questions > 0
    p_agreement = n_agreements / float(n_questions)

    assert 0 <= p_agreement <= 1, "P(Agreement) should be a defined probability"

    # calculate p_expected: the agreement expected by chance
    p_expected = 0.0
    for response in potential_responses:
        p_expected += biasA.freq(response) * biasB.freq(response)
    
    assert 0 <= p_expected <= 1, \
        "P(Expected) should be bewteeen 0 and 1, not %.2f" % p_expected

    # calculate kappa
    kappa = (p_agreement - p_expected)/(1 - p_expected)

    return kappa

#----------------------------------------------------------------------------#

def frange(start, end=None, inc=None):
    """
    A range function, that does accept float increments...
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66472

        >>> frange(1.0, 3.0, 0.5)
        [1.0, 1.5, 2.0, 2.5]
    """ 

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L

#----------------------------------------------------------------------------#

def inclusion_combinations(sequence):
    """
    Returns a list of all combinations of inclusion/exclusion of the
    elements of the given sequence.

        >>> inclusion_combinations([])
        [[]]
        >>> inclusion_combinations([1, 2])
        [[], [1], [2], [1, 2]]
    """
    current_combs = [[]]
    for element in sequence:
        next_set = []
        for comb in current_combs:
            next_set.append(comb + [element])

        current_combs += next_set

    return current_combs

#----------------------------------------------------------------------------#

def mean(values):
    """
    Returns the mean of a sequence of values. If the sequence is empty, raises
    an InsufficientData error.

        >>> mean([1, 2, 3])
        2.0
    """
    values_iter = iter(values)
    n = 1

    # Need at least one value.
    try:
        total = values_iter.next()
    except StopIteration:
        raise InsufficientData

    for value in values_iter:
        total += value
        n += 1

    return total / float(n)

#----------------------------------------------------------------------------#

def stddev(values):
    """
    Returns the standard deviation of a sequence of values. If less than three
    values are provided, raises an InsufficientData error.
    """
    values_iter = iter(values)
    try:
        value = values_iter.next()
    except StopIteration:
        raise InsufficientData

    total = value
    total_squared = value * value
    n = 1

    for value in values_iter:
        total += value
        total_squared += value * value
        n += 1

    # Need at least two values.
    if n < 2:
        raise InsufficientData

    n = float(n)
    return sqrt((total_squared - total * total / n) / (n - 1))

#----------------------------------------------------------------------------#

def basic_stats(values):
    """
    Returns the mean and standard deviation of the sample as a tuple.
    """
    values_iter = iter(values)
    try:
        value = values_iter.next()
    except StopIteration:
        raise InsufficientData

    total = value
    total_squared = value * value
    n = 1

    for value in values_iter:
        total += value
        total_squared += value * value
        n += 1

    n = float(n)
    if n > 2:
        stddev_val = sqrt((total_squared - total * total / n) / (n - 1))
    else:
        stddev_val = None

    mean_val = total / n

    return (mean_val, stddev_val)

#----------------------------------------------------------------------------#

def is_nan(x):
    """
    Returns True if the number is NaN, False otherwise.

    >>> x = 1e300
    >>> is_nan(x)
    False
    >>> inf = x*x
    >>> is_nan(inf)
    False
    >>> nan = inf - inf
    >>> is_nan(nan)
    True
    """
    x = float(x)
    if max(x, 1e10) is x and min(x, -1e10) is x:
        return True
    else:
        return False

#----------------------------------------------------------------------------#

