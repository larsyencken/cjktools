# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# test_table.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Mar 13 16:42:43 2006
#
#----------------------------------------------------------------------------# 

import os, sys, unittest
import doctest
from table import *

#----------------------------------------------------------------------------#

def suite():
    test_suite = unittest.TestSuite((
            unittest.makeSuite(IntListPackingTestCase),
            unittest.makeSuite(TableTestCase),
            unittest.makeSuite(TableAndFieldTest),
        ))
    return test_suite

#----------------------------------------------------------------------------#

class IntListPackingTestCase(unittest.TestCase):
    """
    This class tests the int_list_pack() and int_list_unpack() methods.
    """
    def setUp(self):
        self.dataA = [1, 2, 3, 5, 6, 7, 9]
        self.dataA_packed = '1-3,5-7,9'
        return

    def test_empty_list(self):
        """
        Test packing and unpacking an empty list.
        """
        self.assertEqual(int_list_pack([]), '')
        self.assertEqual(int_list_unpack(''), [])

        return

    def test_border_cases(self):
        self.assertEqual(int_list_pack([1000]), '1000')
        self.assertEqual(int_list_unpack('1000'), [1000])

        return
    
    def test_pack_and_unpack(self):
        """
        Test a generic pack and unpack.
        """
        packed_data = int_list_pack(self.dataA)
        self.assertEqual(packed_data, self.dataA_packed)
        self.assertEqual(int_list_unpack(packed_data), self.dataA)
        return
 
#----------------------------------------------------------------------------#

class TableTestCase(unittest.TestCase):
    """
    This class tests the Table class. 
    """
    def setUp(self):
        self.row_labels = ['a', 'b', 'c']
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

        self.combined_data = [
                ('1.0', 'cow', '2.0', 'COW'),
                ('sheep', '2.0', 'SHEEP', '3.0'),
                ('ox', 'tail', 'LAMB', 'TAIL')
            ]

        self.dummy_file = 'tmp_test.csv'
        pass

    #------------------------------------------------------------------------#

    def _generate_block_a(self):
        x = CsvBlock('woof', self.row_labels, ['apple', 'boar'])
        for row in self.dataA:
            x.add_row(row)
        return x
    
    #------------------------------------------------------------------------#

    def _generate_block_b(self):
        x = CsvBlock('woof', self.row_labels, ['apple', 'boar'])
        for row in self.dataB:
            x.add_row(row)
        return x
    
    #------------------------------------------------------------------------#

    def test_block(self):
        blockA = self._generate_block_a()

        self.assertEqual(blockA.width(), 2)
        self.assertEqual(blockA.height(), 3)
        self.assertEqual(blockA._rows, self.dataA)

        return
    
    #------------------------------------------------------------------------#

    def test_combine(self):
        blockA = self._generate_block_a()
        blockB = self._generate_block_b()

        table = CsvTable(self.dummy_file)
        table.add_block(blockA)
        table.add_block(blockB)
        table.flush()
        del table

        reader = csv.reader(open(self.dummy_file))

        header = tuple(reader.next())
        self.assertEqual(header, ('',) + ('woof', '')*2)
        subheader = tuple(reader.next())
        self.assertEqual(subheader, ('',) + ('apple', 'boar')*2)

        row_labels = self.row_labels[:]
        for desired_row, actual_row in zip(self.combined_data, reader):
            desired_row = list(desired_row)
            actual_row = list(actual_row)
            self.assertEqual(actual_row.pop(0), row_labels.pop(0))
            self.assertEqual(actual_row, desired_row)

        return

    #------------------------------------------------------------------------#

    def tearDown(self):
        if os.path.exists(self.dummy_file):
            os.remove(self.dummy_file)
            pass
        return

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

class TableAndFieldTest(unittest.TestCase):
    def setUp(self):
        self.table_a_header = ['a', 'b']
        self.table_a_data = [(1,2),(3,4),(5,6),(0,0)]
        return

    def test_table_to_fields(self):
        """
        The table_to_fields() and fields_to_table() methods
        """
        fields = table_to_fields(self.table_a_header, self.table_a_data)
        self.assertEqual(fields, [
                {'a': 1, 'b': 2},
                {'a': 3, 'b': 4},
                {'a': 5, 'b': 6},
                {'a': 0, 'b': 0}
            ])

        header, data = fields_to_table(fields)

        self.assertEqual(header, self.table_a_header)
        self.assertEqual(data, self.table_a_data)

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:

