# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# testTable.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Mar 13 16:42:43 2006
#
#----------------------------------------------------------------------------# 

import os, sys, unittest
import doctest
from table import *

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(IntListPackingTestCase),
            unittest.makeSuite(TableTestCase),
            unittest.makeSuite(TableAndFieldTest),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class IntListPackingTestCase(unittest.TestCase):
    """
    This class tests the intListPack() and intListUnpack() methods.
    """
    def setUp(self):
        self.dataA = [1, 2, 3, 5, 6, 7, 9]
        self.dataA_packed = '1-3,5-7,9'
        return

    def testEmptyList(self):
        """
        Test packing and unpacking an empty list.
        """
        self.assertEqual(intListPack([]), '')
        self.assertEqual(intListUnpack(''), [])

        return

    def testBorderCases(self):
        self.assertEqual(intListPack([1000]), '1000')
        self.assertEqual(intListUnpack('1000'), [1000])

        return
    
    def testPackAndUnpack(self):
        """
        Test a generic pack and unpack.
        """
        packedData = intListPack(self.dataA)
        self.assertEqual(packedData, self.dataA_packed)
        self.assertEqual(intListUnpack(packedData), self.dataA)
        return
 
#----------------------------------------------------------------------------#

class TableTestCase(unittest.TestCase):
    """
    This class tests the Table class. 
    """
    def setUp(self):
        self.rowLabels = ['a', 'b', 'c']
        self.dataA = [
                ('1.0', 'cow'),
                ('sheep', '2.0'),
                ('ox', 'tail')
            ]

        self.dataB = [
                ('2.0', 'COW'),
                ('SHEEP', '3.0'),
                ('LAMB', 'TAIL')
            ]

        self.combinedData = [
                ('1.0', 'cow', '2.0', 'COW'),
                ('sheep', '2.0', 'SHEEP', '3.0'),
                ('ox', 'tail', 'LAMB', 'TAIL')
            ]

        self.dummyFile = 'tmpTest.csv'
        pass

    #------------------------------------------------------------------------#

    def _generateBlockA(self):
        x = CsvBlock('woof', self.rowLabels, ['apple', 'boar'])
        for row in self.dataA:
            x.addRow(row)
        return x
    
    #------------------------------------------------------------------------#

    def _generateBlockB(self):
        x = CsvBlock('woof', self.rowLabels, ['apple', 'boar'])
        for row in self.dataB:
            x.addRow(row)
        return x
    
    #------------------------------------------------------------------------#

    def testBlock(self):
        blockA = self._generateBlockA()

        self.assertEqual(blockA.width(), 2)
        self.assertEqual(blockA.height(), 3)
        self.assertEqual(blockA._rows, self.dataA)

        return
    
    #------------------------------------------------------------------------#

    def testCombine(self):
        blockA = self._generateBlockA()
        blockB = self._generateBlockB()

        table = CsvTable(self.dummyFile)
        table.addBlock(blockA)
        table.addBlock(blockB)
        table.flush()
        del table

        reader = csv.reader(open(self.dummyFile))

        header = tuple(reader.next())
        self.assertEqual(header, ('',) + ('woof', '')*2)
        subheader = tuple(reader.next())
        self.assertEqual(subheader, ('',) + ('apple', 'boar')*2)

        rowLabels = self.rowLabels[:]
        for desiredRow, actualRow in zip(self.combinedData, reader):
            desiredRow = list(desiredRow)
            actualRow = list(actualRow)
            self.assertEqual(actualRow.pop(0), rowLabels.pop(0))
            self.assertEqual(actualRow, desiredRow)

        return

    #------------------------------------------------------------------------#

    def tearDown(self):
        if os.path.exists(self.dummyFile):
            os.remove(self.dummyFile)
            pass
        return

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

class TableAndFieldTest(unittest.TestCase):
    def setUp(self):
        self.tableAHeader = ['a', 'b']
        self.tableAData = [(1,2),(3,4),(5,6),(0,0)]
        return

    def testTableToFields(self):
        """
        The tableToFields() and fieldsToTable() methods
        """
        fields = tableToFields(self.tableAHeader, self.tableAData)
        self.assertEqual(fields, [
                {'a': 1, 'b': 2},
                {'a': 3, 'b': 4},
                {'a': 5, 'b': 6},
                {'a': 0, 'b': 0}
            ])

        header, data = fieldsToTable(fields)

        self.assertEqual(header, self.tableAHeader)
        self.assertEqual(data, self.tableAData)

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

