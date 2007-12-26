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

    def __init__(self, forwardLabel=None, reverseLabel=None):
        """
        Constructor.
        """
        self.forwardLabel = forwardLabel
        self.reverseLabel = reverseLabel

        self._forwardMap = {}
        self._reverseMap = {}

        return

    #------------------------------------------------------------------------#
   
    def fromSequence(self, sequence):
        """
        Loads the sequence from (aVal, bVal) pairs.
        """
        for aVal, bVal in sequence:
            self.add(aVal, bVal)

        return self

    #------------------------------------------------------------------------#

    def add(self, aVal, bVal):
        """
        Adds a pair to the relation.
        """
        if aVal in self._forwardMap:
            self._forwardMap[aVal].add(bVal)
        else:
            self._forwardMap[aVal] = set([bVal])

        if bVal in self._reverseMap:
            self._reverseMap[bVal].add(aVal)
        else:
            self._reverseMap[bVal] = set([aVal])

        return self

    #------------------------------------------------------------------------#

    def remove(self, aVal, bVal):
        """
        Removes a pair from the relation.
        """
        self._forwardMap[aVal].remove(bVal)
        self._reverseMap[bVal].remove(aVal)
        return self

    #------------------------------------------------------------------------#

    def inASet(self, aVal):
        return aVal in self._forwardMap

    #------------------------------------------------------------------------#

    def inBSet(self, bVal):
        return bVal in self._reverseMap

    #------------------------------------------------------------------------#

    def forwardGet(self, aVal):
        result = self._forwardMap.get(aVal)
        if result is None:
            return set()
        else:
            return set(result)

    #------------------------------------------------------------------------#

    def reverseGet(self, bVal):
        result = self._reverseMap.get(bVal)
        if result is None:
            return set()
        else:
            return set(result)

    #------------------------------------------------------------------------#

    def __contains__(self, pair):
        """
        Tests whether the pair is contained in the relation.
        """
        aVal, bVal = pair
        return aVal in self._forwardMap and \
                bVal in self._forwardMap.__getitem__(aVal)

    #------------------------------------------------------------------------#

    def merge(self, rhs):
        """
        Return a new relation which is the result of merging this
        relation with the rhs.
        """
        if self.forwardLabel == rhs.forwardLabel and \
                self.reverseLabel == rhs.reverseLabel:
            return Relation(self.forwardLabel, self.reverseLabel).fromSequence(
                    itertools.chain(self.iteritems(), rhs.iteritems())
                )
        else:
            return Exception, "Cannot merge relations with different labels"

    #------------------------------------------------------------------------#

    def toSequence(self):
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
        return sum(itertools.imap(len, self._forwardMap.itervalues()))

    #------------------------------------------------------------------------#
    
    def iteritems(self):
        """
        Returns an iterator over all pairs in the dictionary.
        """
        for aVal, bValues in self._forwardMap.iteritems():
            for bVal in bValues:
                yield aVal, bVal

        return

    #------------------------------------------------------------------------#

    def __repr__(self):
        return '<Relation %s <-> %s, %d pairs>' % (
                self.forwardLabel,
                self.reverseLabel,
                len(self),
            )

    #------------------------------------------------------------------------#

    def isSubRelation(self, rhs):
        """
        Returns True if the pairs contained in this relation are a
        subset of the pairs in the rhs relation.

        @type rhs: Relation
        """
        return set(self.iteritems()).issubset(rhs.iteritems())

    #------------------------------------------------------------------------#

    def isSuperRelation(self, rhs):
        """
        Returns True if the pairs contained in this relation are a
        superset of the pairs in the rhs relation.

        @type rhs: Relation
        """
        return set(self.iteritems()).issuperset(rhs.iteritems())

    #------------------------------------------------------------------------#

    def forwardMap(self):
        return self._forwardMap.copy()

    #------------------------------------------------------------------------#

    def reverseMap(self):
        return self._reverseMap.copy()

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

    def add(self, aVal, bVal, score):
        """
        Adds a scored value to the relation.
        """
        Relation.add(self, aVal, bVal)
        self._scores[(aVal, bVal)] = score
        return self

    #------------------------------------------------------------------------#

    def remove(self, aVal, bVal):
        Relation.remove(self, aVal, bVal)
        del self._scores[(aVal, bVal)]
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
        aVal, bVal = pair
        return (aVal, bVal) in self._scores

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

    def forwardGet(self, aVal):
        values = Relation.forwardGet(self, aVal)
        results = dict((v, self._scores[(aVal, v)]) for v in values)
        return results

    #------------------------------------------------------------------------#

    def reverseGet(self, bVal):
        values = Relation.reverseGet(self, bVal)
        results = dict((v, self._scores[(v, bVal)]) for v in values)
        return results

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#
    
    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
