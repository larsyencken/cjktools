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

    def get_children(self):
        return self.values()

    children = property(get_children)

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
        o_stream = sopen(filename, 'w')
        for depth, place in self.walk():
            print >> o_stream, place._to_line(depth)
        o_stream.close()
        return

    #------------------------------------------------------------------------#

    @classmethod
    def from_file(cls, filename):
        """
        Construct a new place hierarchy from the given filename.
        """
        i_stream = sopen(filename)
        lines = iter(enumerate(i_stream))

        depth, root_node = cls._from_line(lines.next()[1])
        if depth != 0:
            raise Exception, "File %s should start with a root node" % filename

        path = [root_node]
        last_depth = depth
        last_node = root_node
        for line_no, line in lines:
            depth, node = cls._from_line(line)
            if depth == last_depth + 1:
                # One level deeper, the last node was the parent.
                path.append(last_node)

            elif depth == last_depth:
                # Same level, same parent.
                pass

            elif depth < last_depth:
                # Up one or more levels.
                depth_diff = last_depth - depth
                path = path[:-depth_diff]

            else:
                raise Exception, "Strange depth found %s (line %d)" % (
                        filename,
                        line_no + 1
                    )

            path[-1].append(node)
            last_node = node
            last_depth = depth

        i_stream.close()

        return root_node

    #------------------------------------------------------------------------#

    def append(self, node):
        """
        Simulate a list appending.
        """
        self[node.label] = node
        return

    #------------------------------------------------------------------------#

    def find_node(self, label):
        """
        Searches for the given node name in a breadth first manner.
        Returns a (node, path) tuple.
        """
        if label == self.label:
            return []

        next_frontier = []
        frontier = [([], self)]

        while frontier or next_frontier:
            while frontier:
                current_path, next_node = frontier.pop()
                if label in next_node:
                    # Success!
                    target_node = next_node[label]
                    target_path = current_path + [label]
                    return target_node, target_path
                else:
                    for new_label, new_node in next_node.iteritems():
                        next_frontier.append(
                                (current_path + [new_label], new_node)
                            )
            else:
                frontier = next_frontier
                next_frontier = []
                random.shuffle(frontier)

        raise KeyError, 'No such node %s' % label

    #------------------------------------------------------------------------#

    def find_all(self, label):
        """
        Finds all nodes which match the given label.
        """
        results = []

        for path, node in self.walk_with_path():
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
        output_stack = [(0, self)]
        output_stack.reverse()
        while output_stack:
            depth, place = output_stack.pop()
            yield depth, place
            children = [(depth+1, p) for p in place.values()]
            children.reverse()
            output_stack.extend(children)
        
        return

    #------------------------------------------------------------------------#

    def walk_with_path(self):
        """
        Returns an iterator over the entire tree. Each node is iterated
        over as a (path, node) pair.
        """
        path = []
        last_depth = 0
        last_node = None
        for depth, node in self.walk():
            if depth == last_depth + 1:
                # One level deeper, the last node was the parent.
                path.append(last_node.label)

            elif depth == last_depth:
                # Same level, same parent.
                pass

            elif depth < last_depth:
                # Up one or more levels.
                depth_diff = last_depth - depth
                path = path[:-depth_diff]

            else:
                raise Exception, "Strange depth found %s (line %d)" % (
                        filename,
                        line_no + 1
                    )

            yield '/'.join(path), node

            last_node = node
            last_depth = depth

        return

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#

    def _to_line(self, depth):
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
    def _from_line(line):
        """
        Parses a single line, returning a (depth, Place) pair.
        """
        line_objs = line.rstrip().split()
        if len(line_objs) == 3:
            depth, label, reading = line_objs
            depth = int(depth)
            if reading == 'None':
                reading = None
            return depth, Place(label, reading)

        elif len(line_objs) == 4:
            depth, label, reading, aliases = line_objs
            depth = int(depth)
            if reading == 'None':
                reading = None
            aliases = aliases.split(':')
            return depth, Place(label, reading, aliases)

        else:
            raise ValueError, "Can't parse line %s" % line

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
