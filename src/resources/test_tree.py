# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_tree.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Fri Jul 27 14:59:05 2007
#
#----------------------------------------------------------------------------# 

import unittest
from tree import TreeNode

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(TreeTestCase),
        ))
    return test_suite

#----------------------------------------------------------------------------#

class TreeTestCase(unittest.TestCase):
    """This class tests the Tree class."""

    def setUp(self):
        root = TreeNode('fruit')
        root.add_child(TreeNode('lemon'))
        root.add_child(TreeNode('strawberry'))
        self.fruit = root
        pass

    def test_walk_preorder(self):
        nodes = [n for n in self.fruit.walk()]
        self.assertEqual(nodes[0], self.fruit)
        self.assertEqual(nodes[1], self.fruit.children['lemon'])
        self.assertEqual(nodes[2], self.fruit.children['strawberry'])
        pass
    
    def test_walk_postorder(self):
        nodes = [n for n in self.fruit.walk_postorder()]
        self.assertEqual(nodes[0], self.fruit.children['lemon'])
        self.assertEqual(nodes[1], self.fruit.children['strawberry'])
        self.assertEqual(nodes[2], self.fruit)
        pass

    def test_prune(self):
        x = self.fruit.copy().prune(lambda n: 'y' not in n.label)
        self.assertEqual(x.label, 'fruit')
        self.assertEqual(x.children.values(), [self.fruit.children['lemon']])

    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

