# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# place.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Sat Jun  9 14:29:29 2007
#
#----------------------------------------------------------------------------#

"""
A data form for storing and manipulating place data.
"""

#----------------------------------------------------------------------------#

import random

from cjktools.common import sopen

#----------------------------------------------------------------------------#

class Place(dict):
    """
    A location or region and its associated label. It may contain other
    locations or regions within it.
    """

    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, label, reading=None, aliases=None):
        """
        Constructor.
        """
        # Add restrictions imposed by our storage format.
        if ' ' in label or \
                (reading and ' ' in reading) or \
                (aliases and ' ' in ''.join(aliases)):
            raise ValueError, "No spaces allowed in place details"

        assert type(label) in (str, unicode), \
                "Expected string, not %s" % `label`

        dict.__init__(self)
        self.label = label
        self.reading = reading
        self.aliases = aliases
        return

    #------------------------------------------------------------------------#

    def getChildren(self):
        return self.values()

    children = property(getChildren)

    #------------------------------------------------------------------------#

    def __repr__(self): 
        return unicode(self)

    #------------------------------------------------------------------------#

    def __unicode__(self):
        return '<Place: %s%s %d children>' % (
                self.label,
                (self.reading and ' /%s/' % self.reading or ''),
                len(self),
            )

    #------------------------------------------------------------------------#

    def dump(self, filename):
        """
        Dump this place hierarchy to the given filename.
        """
        oStream = sopen(filename, 'w')
        for depth, place in self.walk():
            print >> oStream, place._toLine(depth)
        oStream.close()
        return

    #------------------------------------------------------------------------#

    @classmethod
    def fromFile(cls, filename):
        """
        Construct a new place hierarchy from the given filename.
        """
        iStream = sopen(filename)
        lines = iter(enumerate(iStream))

        depth, rootNode = cls._fromLine(lines.next()[1])
        if depth != 0:
            raise Exception, "File %s should start with a root node" % filename

        path = [rootNode]
        lastDepth = depth
        lastNode = rootNode
        for lineNo, line in lines:
            depth, node = cls._fromLine(line)
            if depth == lastDepth + 1:
                # One level deeper, the last node was the parent.
                path.append(lastNode)

            elif depth == lastDepth:
                # Same level, same parent.
                pass

            elif depth < lastDepth:
                # Up one or more levels.
                depthDiff = lastDepth - depth
                path = path[:-depthDiff]

            else:
                raise Exception, "Strange depth found %s (line %d)" % (
                        filename,
                        lineNo + 1
                    )

            path[-1].append(node)
            lastNode = node
            lastDepth = depth

        iStream.close()

        return rootNode

    #------------------------------------------------------------------------#

    def append(self, node):
        """
        Simulate a list appending.
        """
        self[node.label] = node
        return

    #------------------------------------------------------------------------#

    def findNode(self, label):
        """
        Searches for the given node name in a breadth first manner.
        Returns a (node, path) tuple.
        """
        if label == self.label:
            return []

        nextFrontier = []
        frontier = [([], self)]

        while frontier or nextFrontier:
            while frontier:
                currentPath, nextNode = frontier.pop()
                if label in nextNode:
                    # Success!
                    targetNode = nextNode[label]
                    targetPath = currentPath + [label]
                    return targetNode, targetPath
                else:
                    for newLabel, newNode in nextNode.iteritems():
                        nextFrontier.append(
                                (currentPath + [newLabel], newNode)
                            )
            else:
                frontier = nextFrontier
                nextFrontier = []
                random.shuffle(frontier)

        raise KeyError, 'No such node %s' % label

    #------------------------------------------------------------------------#

    def findAll(self, label):
        """
        Finds all nodes which match the given label.
        """
        results = []

        for path, node in self.walkWithPath():
            if node.label == label:
                results.append( (path, node) )

        return results

    #------------------------------------------------------------------------#

    def walk(self):
        """
        Returns an iterator over the entire tree, yielding nodes in order
        in (depth, node) pairs.
        """
        # Use an output stack to avoid recursion. The reverse() calls ensure
        # that they get re-parsed in the same order they came out.
        outputStack = [(0, self)]
        outputStack.reverse()
        while outputStack:
            depth, place = outputStack.pop()
            yield depth, place
            children = [(depth+1, p) for p in place.values()]
            children.reverse()
            outputStack.extend(children)
        
        return

    #------------------------------------------------------------------------#

    def walkWithPath(self):
        """
        Returns an iterator over the entire tree. Each node is iterated
        over as a (path, node) pair.
        """
        path = []
        lastDepth = 0
        lastNode = None
        for depth, node in self.walk():
            if depth == lastDepth + 1:
                # One level deeper, the last node was the parent.
                path.append(lastNode.label)

            elif depth == lastDepth:
                # Same level, same parent.
                pass

            elif depth < lastDepth:
                # Up one or more levels.
                depthDiff = lastDepth - depth
                path = path[:-depthDiff]

            else:
                raise Exception, "Strange depth found %s (line %d)" % (
                        filename,
                        lineNo + 1
                    )

            yield '/'.join(path), node

            lastNode = node
            lastDepth = depth

        return

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#

    def _toLine(self, depth):
        """
        Given a depth, returns an output line as a string.
        """
        if self.aliases:
            return '%d %s %s %s' % (depth, self.label, self.reading,
                    self.aliases)
        else:
            return '%d %s %s' % (depth, self.label, self.reading)
    
    #------------------------------------------------------------------------#

    @staticmethod
    def _fromLine(line):
        """
        Parses a single line, returning a (depth, Place) pair.
        """
        lineObjs = line.rstrip().split()
        if len(lineObjs) == 3:
            depth, label, reading = lineObjs
            depth = int(depth)
            if reading == 'None':
                reading = None
            return depth, Place(label, reading)

        elif len(lineObjs) == 4:
            depth, label, reading, aliases = lineObjs
            depth = int(depth)
            if reading == 'None':
                reading = None
            aliases = aliases.split(':')
            return depth, Place(label, reading, aliases)

        else:
            raise ValueError, "Can't parse line %s" % line

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
