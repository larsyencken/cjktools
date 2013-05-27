# -*- coding: utf-8 -*-
#
#  test_tree.py
#  cjktools
#

import unittest

from tree import TreeNode


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(TreeTestCase),
    ))
    return test_suite


class TreeTestCase(unittest.TestCase):
    def setUp(self):
        root = TreeNode('fruit')
        root.add_child(TreeNode('lemon'))
        root.add_child(TreeNode('strawberry'))
        self.fruit = root

    def test_walk_preorder(self):
        nodes = [n for n in self.fruit.walk()]
        self.assertEqual(nodes[0], self.fruit)
        self.assertEqual(nodes[1], self.fruit.children['lemon'])
        self.assertEqual(nodes[2], self.fruit.children['strawberry'])

    def test_walk_postorder(self):
        nodes = [n for n in self.fruit.walk_postorder()]
        self.assertEqual(nodes[0], self.fruit.children['lemon'])
        self.assertEqual(nodes[1], self.fruit.children['strawberry'])
        self.assertEqual(nodes[2], self.fruit)

    def test_prune(self):
        x = self.fruit.copy().prune(lambda n: 'y' not in n.label)
        self.assertEqual(x.label, 'fruit')
        self.assertEqual(x.children.values(), [self.fruit.children['lemon']])


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
