# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import unittest

from KicadModTree.nodes.Node import *


class HelperTestChildNode(Node):
    def __init__(self):
        Node.__init__(self)


class NodeTests(unittest.TestCase):

    def testInit(self):
        node = Node()
        self.assertIs(node.getParent(), None)
        self.assertIs(node.getRootNode(), node)
        self.assertEqual(len(node.getNormalChilds()), 0)
        self.assertEqual(len(node.getVirtualChilds()), 0)
        self.assertEqual(len(node.getAllChilds()), 0)

    def testAppend(self):
        node = Node()
        self.assertEqual(len(node.getNormalChilds()), 0)

        childNode1 = Node()
        node.append(childNode1)
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 1)

        childNode2 = Node()
        node.append(childNode2)
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 2)

        with self.assertRaises(TypeError):
            node.append(None)
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 2)

        with self.assertRaises(TypeError):
            node.append(object)
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 2)

        with self.assertRaises(TypeError):
            node.append("a string is not a node object")
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 2)

        with self.assertRaises(MultipleParentsError):
            node.append(childNode1)
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 2)

        childNode3 = HelperTestChildNode()
        node.append(childNode3)
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertIn(childNode3, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(childNode3.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 3)

    def testExtend(self):
        node = Node()
        self.assertEqual(len(node.getNormalChilds()), 0)

        childNode1 = Node()
        childNode2 = Node()
        node.extend([childNode1, childNode2])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 2)

        childNode3 = Node()
        node.extend([childNode3])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertIn(childNode3, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(childNode3.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 3)

        node.extend([])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertIn(childNode3, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(childNode3.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 3)

        with self.assertRaises(TypeError):
            node.extend([None])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertIn(childNode3, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(childNode3.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 3)

        with self.assertRaises(TypeError):
            node.append([object])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertIn(childNode3, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(childNode3.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 3)

        with self.assertRaises(TypeError):
            node.append(["a string is not a node object"])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertIn(childNode3, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(childNode3.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 3)

        with self.assertRaises(MultipleParentsError):
            node.extend([childNode1])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertIn(childNode3, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(childNode3.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 3)

        childNode4 = Node()
        childNode5 = Node()
        with self.assertRaises(MultipleParentsError):
            node.extend([childNode4, childNode5, childNode5])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertIn(childNode3, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(childNode3.getParent(), node)
        self.assertEqual(childNode4.getParent(), None)
        self.assertEqual(childNode5.getParent(), None)
        self.assertEqual(len(node.getNormalChilds()), 3)

    def testRemove(self):
        node = Node()
        self.assertEqual(len(node.getNormalChilds()), 0)

        childNode1 = Node()
        childNode2 = Node()
        node.extend([childNode1, childNode2])
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 2)

        node.remove(childNode1)
        self.assertNotIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), None)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 1)

        node.remove(childNode1)
        self.assertNotIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), None)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 1)

        with self.assertRaises(TypeError):
            node.remove([None])
        self.assertNotIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), None)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 1)

        with self.assertRaises(TypeError):
            node.remove([object])
        self.assertNotIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), None)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 1)

        with self.assertRaises(TypeError):
            node.remove(["a string is not a node object"])
        self.assertNotIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), None)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 1)

    def testInsert(self):
        node = Node()
        self.assertEqual(len(node.getNormalChilds()), 0)

        childNode1 = Node()
        node.insert(childNode1)
        self.assertIn(childNode1, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 1)

        childNode2 = Node()
        node.insert(childNode2)
        self.assertIn(childNode1, childNode2.getNormalChilds())
        self.assertNotIn(childNode1, node.getNormalChilds())
        self.assertIn(childNode2, node.getNormalChilds())
        self.assertEqual(childNode1.getParent(), childNode2)
        self.assertEqual(childNode2.getParent(), node)
        self.assertEqual(len(node.getNormalChilds()), 1)
        self.assertEqual(len(childNode1.getNormalChilds()), 0)
        self.assertEqual(len(childNode2.getNormalChilds()), 1)

    def testInsertWithManyChilds(self):
        node = Node()
        self.assertEqual(len(node.getNormalChilds()), 0)

        for i in range(0, 200):
            node.append(Node())

        insertNode = Node()
        self.assertEqual(len(node.getNormalChilds()), 200)
        self.assertEqual(len(insertNode.getNormalChilds()), 0)
        node.insert(insertNode)
        self.assertEqual(len(node.getNormalChilds()), 1)
        self.assertEqual(len(insertNode.getNormalChilds()), 200)
