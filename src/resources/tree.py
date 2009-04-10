# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# tree.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Thu Jul 26 16:52:28 2007
#
#----------------------------------------------------------------------------#

"""
An abstract tree datatype.
"""

#----------------------------------------------------------------------------#

from random import shuffle

#----------------------------------------------------------------------------#

class TreeNode(object):
    """
    A node in a hierarchical labelled tree. Each node contains links both
    downwards to children and upwards to a unique parent.
    """
    __slots__ = ('label', 'children', 'attrib', 'parent')

    def __init__(self, label, children=None, attrib=None, parent=None):
        self.label = label
        self.children = children or {}
        self.attrib = attrib or {}
        self.parent = parent

    def get_ancestors(self):
        result = [self]
        node = self
        while node.parent is not None:
            result.append(node.parent)
            node = node.parent

        result.reverse()
        return result

    ancestors = property(get_ancestors)

    def get_path(self):
        """
        Returns the path from the root node to this node as a list of
        nodes.
        """
        path = [self]

        node = path[-1]
        while node.parent is not None:
            path.append(node.parent)
            node = path[-1]

        path.reverse()
        return path
    
    path = property(get_path)

    def walk_preorder(self):
        """
        Walks the tree in a pre-order manner. At every node, it yields a tuple
        (path, node), where path is a list of all ancestor nodes from highest
        lowest.
        """
        stack = [self]
        while stack:
            node = stack.pop()
            yield node
            stack.extend(node.children.values())

        return

    def walk(self):
        return self.walk_preorder()

    def walk_postorder(self):
        """
        Walks the tree in a post-order manner, yielding (path, node) pairs.
        """
        stack = [(self, False)]

        while stack:
            node, visited = stack.pop()

            if visited or not node:
                # Either second pass, or a leaf.
                yield node
            else:
                # First pass, has children.
                stack.append((node, True))
                stack.extend([(c, False) for c in node.children.values()])

        return

    def walk_breadth_first(self):
        """
        Returns an iterator which walks the tree in a breadth-first manner.
        """
        next_frontier = []
        frontier = [self]

        while frontier:
            node = frontier.pop()
            yield node

            for child_node in node.children.values():
                next_frontier.append(child_node)

            if not frontier:
                # Exhausted this depth, so go deeper if possible.
                frontier = next_frontier
                next_frontier = []
                shuffle(frontier)

        return

    def unlink(self):
        """Unlink this node from its parent."""
        if self.parent:
            del self.parent.children[self.label]
        self.parent = None
        return

    def copy(self):
        """
        Returns a copy of the tree structure (but not the node values).
        """
        if self.parent:
            raise Exception, "Cannot copy from a non-root node"

        new_root = TreeNode(self.label, self.children.copy(),
                self.attrib.copy())

        stack = [new_root]
        while stack:
            node = stack.pop()
            for child_label, child_node in node.children.items():
                copied_child = TreeNode(
                        child_label,
                        child_node.children.copy(),
                        child_node.attrib.copy(),
                        node,
                    )
                node.children[child_label] = copied_child
                stack.append(copied_child)

        return new_root

    def prune(self, predicate):
        """
        Prunes dead subtrees recursively.

        The method passed in is used on each node to determine if it has
        viable children or not. If all nodes are pruned, returns None.
        """
        new_tree = self.copy()
        for node in new_tree.walk_postorder():
            if node.children or predicate(node):
                continue
            else:
                node.unlink()

        if new_tree.children or predicate(new_tree):
            return new_tree
        else:
            return None

    def __len__(self):
        return len(self.children)

    def __str__(self):
        return '<TreeNode: %s (%d children)>' % (self.label, len(self))

    def __repr__(self):
        return str(self)

    def add_child(self, child_node):
        """Adds the child node to this tree."""
        self.children[child_node.label] = child_node
        child_node.parent = self
        return

    def del_child(self, child_node):
        """
        Unlinks the child node from this node, and removes its parent
        pointer.
        """
        del self.children[child_node.label]
        child_node.attrib['parent'] = None
        return

    def get_path(self, path):
        """Get a particular path in the node."""
        if type(path) in (str, unicode):
            path = path.lstrip('/').split('/')
        else:
            assert type(path) == list

        next_node = self

        for label in path:
            next_node = next_node.children[label]

        return next_node

    def find_node(self, label):
        """
        Searches for the given node name in a breadth first manner.
        Returns a (path, node) tuple.
        """
        for node in self.walk_breadth_first():
            if node.label == label:
                return node
        else:
            raise KeyError, label

    def __getitem__(self, key):
        """Returns the attribute matching the given key."""
        return self.attrib.__getitem__(key)
    
    def __setitem__(self, key, value):
        """Saves the attribute value for the given key."""
        return self.attrib.__setitem__(key, value)

    def __contains__(self, key):
        return self.attrib.has_key(key)

    def __delitem__(self, key):
        """Deletes the given attribute."""
        del self.attrib[key]
        return

    def __eq__(self, rhs):
        return self.label == rhs.label and \
                self.attrib == rhs.attrib and \
                self.children == rhs.children

    def build_index(self):
        """
        Builds an index mapping each label to all the nodes which match it
        (potentially more than one).
        """
        index = {}
        for path, node in self.walk():
            if node.label not in index:
                index[node.label] = [node]
            else:
                index[node.label].append(node)

        return index

    def layout(self, method=None):
        """
        Pretty print the tree to stdout. Can optionally pass in a method
        which gets called to represents each node. The default output just
        uses the node's label.
        """
        if method is None:
            method = lambda n: n.label

        print method(self)
        self._layout_children(self, '', method)
        return


    #------------------------------------------------------------------------#
    # PRIVATE
    #------------------------------------------------------------------------#

    def _layout_children(self, node, prefix, method):
        children = node.children.values()
        if not children:
            return

        for child in children[:-1]:
            print '%s├─ %s' % (prefix, method(child))
            self._layout_children(child, prefix + '│  ', method)
        
        child = children[-1]
        print '%s└─ %s' % (prefix, method(child))
        self._layout_children(child, prefix + '   ', method)

        return

#----------------------------------------------------------------------------#

class TreeDist(object):
    """
    A tree probability distribution, initialized by passing in a constructed
    tree which needs annotation.
    """
    #------------------------------------------------------------------------#
    # PUBLIC
    #------------------------------------------------------------------------#

    def __init__(self, root, count_method=len):
        """
        Builds a tree distribution out of the existing tree structure.
        """
        self.root = root.copy()

        if count_method is None:
            return

        # First pass, accumulate counts.
        for node in self.root.walk_postorder():
            node['count'] = count_method(node)
            node['cum_count'] = node['count'] + \
                    sum([c['count'] for c in node.children.values()])

        # Second pass, convert to MLE probabilities, with the assumption that
        # counts propagate upwards.
        total = float(self.root['cum_count'])
        for node in self.root.walk():
            node['freq'] = node['cum_count'] / total

        return

    #------------------------------------------------------------------------#

    def copy(self):
        """Returns a shallow copy of the tree."""
        return TreeDist(self.root.copy(), count_method=None)

    #------------------------------------------------------------------------#

    def layout(self):
        """Prints a graphical representation of the tree to stdout."""
        return self.root.layout(
                method=lambda n: '%s %.04f' % (n.label, n['freq'])
            )

    #------------------------------------------------------------------------#

    def combine(self, rhs, f=lambda x, y: (x + y)/2.0, label='union'):
        """Returns a tree which is topologically the union of the two trees."""
        assert self.tree.label == rhs.tree.label
        new_label = '%s(%s, %s)' % (label, self.label, rhs.label)
        new_tree_dist = TreeDist(new_label)

        new_tree = TreeNode(self.tree.label)

        stack = []
        for key in set(self.tree.keys()).union(rhs.tree.keys()):
            stack.append(
                    (self.tree.get(key), rhs.tree.get(key), new_tree),
                )

        while stack:
            lhs_node, rhs_node, parent = stack.pop()
            if lhs_node is None:
                new_child = rhs_node.copy()
                for old_node, new_node in zip(rhs_node.walk(), new_child.walk()):
                    new_node.freq = f(0.0, old_node.freq)

            elif rhs_node is None:
                new_child = lhs_node.copy()
                for old_node, new_node in zip(lhs_node.walk(), new_child.walk()):
                    new_node.freq = f(old_node.freq, 0.0)

            else:
                new_child = TreeNode(lhs_node.label)
                new_child.freq = f(lhs_node.freq, rhs_node.freq)
                for key in set(lhs_node.keys()).union(rhs_node.keys()):
                    stack.append(
                            (lhs_node.get(key), rhs_node.get(key), new_child),
                        )

            parent.append_child(new_child)

        new_tree_dist.tree = new_tree

        return new_tree_dist

    def union(self, rhs):
        return self.union(rhs, f=lambda x, y: (x + y)/2.0, label='union')

    def diff(self, rhs):
        return self.union(rhs, f=lambda x, y: x - y, label='diff')

#----------------------------------------------------------------------------#
