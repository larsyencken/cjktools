#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# table_data.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Mar 13 12:54:07 EST 2006
#
#----------------------------------------------------------------------------#

"""
Support for converting between tabular and record-style data, and for
outputting auto-wrapped csv data with subcolumns.
"""

#----------------------------------------------------------------------------#

import csv
import types

#----------------------------------------------------------------------------#

def parse_lines(file_stream, separator=' ', n=None):
    """
    An iterator which wraps a filestream, expecting either comment lines
    or space separated values. Yields the tuples.
    """
    if n is None:
        for line in file_stream:
            if line.startswith('#'):
                continue

            yield line.rstrip().split(separator)
    else:
        for line in file_stream:
            if line.startswith('#'):
                continue

            yield line.rstrip().split(separator, n)

    return

#----------------------------------------------------------------------------#

def int_list_pack(int_list):
    """
    Packs a list of integers into a csv string.

        >>> int_list_pack([1, 2, 3, 7])
        '1-3,7'
    """
    if int_list == []:
        # handle an empty list on packing and unpacking
        return ''

    int_list.sort()

    packed_elems = []

    start_range = last_in_range = int_list[0]

    if start_range < 0:
        raise Exception, "Don't deal with negative numbers"

    i = 1
    int_list_len = len(int_list)
    while i < int_list_len:
        while i < int_list_len and int_list[i] == last_in_range + 1:
            last_in_range += 1
            i += 1

        if last_in_range - start_range >= 1:
            # pack in short form
            packed_elems.append('%d-%d' % (start_range, last_in_range))
        else:
            packed_elems.append(str(start_range))

        if i == int_list_len:
            break

        start_range = last_in_range = int_list[i]
        i += 1
    else:
        packed_elems.append(str(start_range))

    return ','.join(packed_elems)

#----------------------------------------------------------------------------#

def int_list_unpack(packed_list):
    """
    Unpacks a packed integer list.

        >>> int_list_unpack('1-3,7')
        [1, 2, 3, 7]
    """
    # handle an empty packed list
    if packed_list == '':
        return []

    packed_items = packed_list.split(',')

    unpacked_elems = []
    for item in packed_items:
        if '-' in item:
            start_range, end_range = item.split('-')
            unpacked_elems.extend(xrange(int(start_range), int(end_range)+1))
        else:
            unpacked_elems.append(int(item))
    
    return unpacked_elems

#----------------------------------------------------------------------------#

def flatten_once(item_list):
    """
    Performs a single flatten on the given data list.

    @param item_list: The original data list.
    @return: A new list containing the same items, but with one level of
        list structure removed.
    """
    new_item_list = []
    for item in item_list:
        if type(item) in (types.ListType, types.TupleType):
            new_item_list.extend(item)
        else:
            new_item_list.append(item)

    return new_item_list

#----------------------------------------------------------------------------#

def group_by_field(key, items, delete_field=False):
    """
    Performs a grouping of the items by key.
    """
    groups = {}
    for item in items:
        key_value = item[key]
        if delete_field:
            del item[key]

        item_list = groups.setdefault(key_value, [])
        item_list.append(item)
    
    return groups

#----------------------------------------------------------------------------#

def field_hierarchy(field_names, record_list, delete_field=False):
    """
    The same as group_by_field(), but it deletes the field key afterwards.
    """
    if len(field_names) == 1:
        # recursive base case
        return group_by_field(field_names[0], record_list, delete_field)

    elif len(field_names) > 1:
        # group once then recurse for each key
        grouped_fields = group_by_field(field_names.pop(0), record_list,
                delete_field)
        for field_key in grouped_fields.iterkeys():
            grouped_fields[field_key] = field_hierarchy(field_names,
                    grouped_fields[field_key], delete_field)
        return grouped_fields

    else:
        raise Exception, "Can't group by an empty path"

#----------------------------------------------------------------------------#
  
def table_to_fields(headers, rows):
    """
    Restructures data between table form (a list of headers and rows) and
    field form (a list of key->value row dictionaries).
    """
    field_rows = []

    for row in rows:
        field_rows.append(dict(zip(headers, row)))
    
    return field_rows

#----------------------------------------------------------------------------#

def fields_to_table(field_rows, order=None):
    """
    The reverse transformation to that performed by table_to_fields(). If
    desired, the header fields can be given an order by specifying them in
    a list as the second argument. The number of table columns can be
    reduced by omitting some from the order list.
    """
    # first pass, accumulate unique keys
    headers = set()
    for field_row in field_rows:
        for key in field_row.iterkeys():
            headers.add(key)

    # second pass, create table rows
    if order is None:
        header_list = list(headers)
    else:
        assert set(order).issubset(headers)
        header_list = order

    rows = []
    for field_row in field_rows:
        row = []
        for key in header_list:
            row.append(field_row.get(key))
        rows.append(tuple(row))

    return header_list, rows

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

class CsvTable:
    """
    This class represents a generic data table, with row and column
    labels, and blocks which must be preserved.
    """

    #------------------------------------------------------------------------#

    def __init__(self, output_file, columns_per_line=20):
        """
        Constructor. Needs the labels for all the rows defined in a block.
        """
        self._blocks = []
        self._row_labels = []

        self._current_width = 0

        self._cols_per_line = columns_per_line

        self._lines = []
        self._o_csv = csv.writer(open(output_file, 'w'))
        return

    #------------------------------------------------------------------------#

    def flush(self):
        """
        Flushes all blocks to the given csv file.
        """
        if not self._blocks:
            return

        header_row = ['']
        subheader_row = ['']
        for block in self._blocks:
            header_row.extend(block.header())
            subheader_row.extend(block.subheader())

        self._o_csv.writerow(header_row)
        self._o_csv.writerow(subheader_row)

        block_rows = map(
                flatten_once, 
                apply( zip, [x.rows() for x in self._blocks] )
            )

        for row_label, row in zip(self._row_labels, block_rows):
            self._o_csv.writerow([row_label] + row)

        self._o_csv.writerow([]) # add a black row between blocks

        # delete the blocks now that they've been printed
        self._blocks = []
        self._current_width = 0
        self._row_labels = []

        return

    #------------------------------------------------------------------------#

    def add_block(self, block):
        """
        Adds a block to the file, flushing out as necessary.
        """
        row_labels_match = self._check_row_labels(block.row_labels())
        within_max_cols = block.width() + self._current_width < \
                self._cols_per_line

        if row_labels_match and within_max_cols:
            # all ok, within the maximum number of columns
            self._blocks.append(block)
            self._current_width += block.width()
        else:
            self.flush()

            # must fix labels before adding block
            self._check_row_labels(block.row_labels())

            # add the new block
            self._blocks = [block]
            self._current_width = block.width()

        return

    #------------------------------------------------------------------------#

    def _check_row_labels(self, row_labels):
        """
        Checks to ensure that the given row labels match the existing
        ones. In the case of an empty bock, adds the row labels in.
        Returns True if the labels match (or if the block was empty),
        False otherwise.

        @param row_labels: The new block labels to check against the
            existing labels.
        @return: True if no flush is needed, False otherwise.
        """
        if self._blocks:
            # return True if the labels match
            return self._row_labels == row_labels
        else:
            # set the row labels to these ones
            self._row_labels = row_labels
            return True

    #------------------------------------------------------------------------#

    def __del__(self):
        """
        Deconstructor. Flush final output.
        """
        self.flush()
        return

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

class CsvBlock:
    """
    Defines a contiguous region of a table, encompassing multiple rows and
    columns. A block is typically a self-contained.
    """

    def __init__(self, block_label, row_labels, column_labels):
        self._rows = []

        self._block_label = block_label
        self._row_labels = row_labels
        self._column_labels = column_labels
        self._row_size = None
        return

    #------------------------------------------------------------------------#

    def add_row(self, row):
        """
        Adds a row to the block.
        """
        row_len = len(row)
        desired_size = self._row_size
        if desired_size is not None and row_len != desired_size:
            raise Exception, "The added row is of the wrong size"

        self._rows.append(tuple(row))
        self._row_size = row_len
        return

    #------------------------------------------------------------------------#

    def width(self):
        """
        Returns the number of columns in the block.
        """
        return len(self._column_labels)
    
    #------------------------------------------------------------------------#

    def height(self):
        """
        Determines the number of rows in the block.
        """
        return len(self._row_labels)
    
    #------------------------------------------------------------------------#

    def rows(self):
        """
        Returns the rows for this block.
        """
        return self._rows

    #------------------------------------------------------------------------#

    def same_row_labels(self, rhs_block):
        """
        Determine if two blocks share row labels....
        """
        return self._row_labels == rhs_block._row_labels

    #------------------------------------------------------------------------#

    def row_labels(self):
        return self._row_labels

    #------------------------------------------------------------------------#

    def header(self):
        """
        Returns the block header.
        """
        return [self._block_label] + [""]*(self.width()-1)

    #------------------------------------------------------------------------#

    def subheader(self):
        """
        Returns the block subheader.
        """
        return self._column_labels

    #------------------------------------------------------------------------#

    def dump(self, output_file):
        """
        Dumps this block to a csv file.
        """
        o_csv = csv.writer(open(output_file, 'w'))
        o_csv.writerow(self.header())
        o_csv.writerow(self.subheader())
        for row in self._rows:
            o_csv.writerow(row)

        return

    #------------------------------------------------------------------------#

    def is_empty(self):
        """
        Returns True if the block is filled with only blank spaces, False
        otherwise.
        """
        for row in self._rows:
            for item in row:
                if item != "":
                    return False
        else:
            return True

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

# vim: ts=4 sw=4 sts=4 et tw=78:
