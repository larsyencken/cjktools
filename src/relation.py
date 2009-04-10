# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# relation.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Thu Mar  8 20:08:55 2007
#
#----------------------------------------------------------------------------#

"""
Implements relations, many-to-many mappings.
"""

#----------------------------------------------------------------------------#

import types
import itertools

#----------------------------------------------------------------------------#

class Relation(object):
    """
    Implements a general relation, i.e. a many-to-many mapping.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, forward_label=None, reverse_label=None):
        """
        Constructor.
        """
        self.forward_label = forward_label
        self.reverse_label = reverse_label

        self._forward_map = {}
        self._reverse_map = {}

        return

    #------------------------------------------------------------------------#
   
    def from_sequence(self, sequence):
        """
        Loads the sequence from (a_val, b_val) pairs.
        """
        for a_val, b_val in sequence:
            self.add(a_val, b_val)

        return self

    #------------------------------------------------------------------------#

    def add(self, a_val, b_val):
        """
        Adds a pair to the relation.
        """
        if a_val in self._forward_map:
            self._forward_map[a_val].add(b_val)
        else:
            self._forward_map[a_val] = set([b_val])

        if b_val in self._reverse_map:
            self._reverse_map[b_val].add(a_val)
        else:
            self._reverse_map[b_val] = set([a_val])

        return self

    #------------------------------------------------------------------------#

    def remove(self, a_val, b_val):
        """
        Removes a pair from the relation.
        """
        self._forward_map[a_val].remove(b_val)
        self._reverse_map[b_val].remove(a_val)
        return self

    #------------------------------------------------------------------------#

    def in_a_set(self, a_val):
        return a_val in self._forward_map

    #------------------------------------------------------------------------#

    def in_b_set(self, b_val):
        return b_val in self._reverse_map

    #------------------------------------------------------------------------#

    def forward_get(self, a_val):
        result = self._forward_map.get(a_val)
        if result is None:
            return set()
        else:
            return set(result)

    #------------------------------------------------------------------------#

    def reverse_get(self, b_val):
        result = self._reverse_map.get(b_val)
        if result is None:
            return set()
        else:
            return set(result)

    #------------------------------------------------------------------------#

    def __contains__(self, pair):
        """
        Tests whether the pair is contained in the relation.
        """
        a_val, b_val = pair
        return a_val in self._forward_map and \
                b_val in self._forward_map.__getitem__(a_val)

    #------------------------------------------------------------------------#

    def merge(self, rhs):
        """
        Return a new relation which is the result of merging this
        relation with the rhs.
        """
        if self.forward_label == rhs.forward_label and \
                self.reverse_label == rhs.reverse_label:
            return Relation(self.forward_label, self.reverse_label).from_sequence(
                    itertools.chain(self.iteritems(), rhs.iteritems())
                )
        else:
            return Exception, "Cannot merge relations with different labels"

    #------------------------------------------------------------------------#

    def to_sequence(self):
        """
        Returns the list of pairs which consist this relation.
        """
        return list(self.iteritems())

    #------------------------------------------------------------------------#

    def __iter__(self):
        return self.iteritems()

    #------------------------------------------------------------------------#

    def __len__(self):
        """
        Returns the number of pairs in this relation.
        """
        return sum(itertools.imap(len, self._forward_map.itervalues()))

    #------------------------------------------------------------------------#
    
    def iteritems(self):
        """
        Returns an iterator over all pairs in the dictionary.
        """
        for a_val, b_values in self._forward_map.iteritems():
            for b_val in b_values:
                yield a_val, b_val

        return

    #------------------------------------------------------------------------#

    def __repr__(self):
        return '<Relation %s <-> %s, %d pairs>' % (
                self.forward_label,
                self.reverse_label,
                len(self),
            )

    #------------------------------------------------------------------------#

    def is_sub_relation(self, rhs):
        """
        Returns True if the pairs contained in this relation are a
        subset of the pairs in the rhs relation.

        @type rhs: Relation
        """
        return set(self.iteritems()).issubset(rhs.iteritems())

    #------------------------------------------------------------------------#

    def is_super_relation(self, rhs):
        """
        Returns True if the pairs contained in this relation are a
        superset of the pairs in the rhs relation.

        @type rhs: Relation
        """
        return set(self.iteritems()).issuperset(rhs.iteritems())

    #------------------------------------------------------------------------#

    def forward_map(self):
        return self._forward_map.copy()

    #------------------------------------------------------------------------#

    def reverse_map(self):
        return self._reverse_map.copy()

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#
    
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

class ScoredRelation(Relation):
    """
    A relation where each pair is also scored.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, *args):
        """
        Constructor.
        """
        apply(Relation.__init__, (self,) + args)

        self._scores = {}
        return

    #------------------------------------------------------------------------#

    def add(self, a_val, b_val, score):
        """
        Adds a scored value to the relation.
        """
        Relation.add(self, a_val, b_val)
        self._scores[(a_val, b_val)] = score
        return self

    #------------------------------------------------------------------------#

    def remove(self, a_val, b_val):
        Relation.remove(self, a_val, b_val)
        del self._scores[(a_val, b_val)]
        return self

    #------------------------------------------------------------------------#

    def iteritems(self):
        for pair in Relation.iteritems(self):
            score = self._score[pair]
            yield pair[0], pair[1], score
        
        return

    #------------------------------------------------------------------------#

    def __contains__(self, pair):
        """
        Check for containership.
        """
        a_val, b_val = pair
        return (a_val, b_val) in self._scores

    #------------------------------------------------------------------------#

    def __iter__(self):
        return self.iteritems()

    #------------------------------------------------------------------------#

    def __getitem__(self, pair):
        """
        Return the score for the pair.
        """
        return self._scores[pair]

    #------------------------------------------------------------------------#

    def forward_get(self, a_val):
        values = Relation.forward_get(self, a_val)
        results = dict((v, self._scores[(a_val, v)]) for v in values)
        return results

    #------------------------------------------------------------------------#

    def reverse_get(self, b_val):
        values = Relation.reverse_get(self, b_val)
        results = dict((v, self._scores[(v, b_val)]) for v in values)
        return results

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#
    
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
