#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# tableData.py
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

def parseLines(fileStream, separator=' ', n=None):
    """
    An iterator which wraps a filestream, expecting either comment lines
    or space separated values. Yields the tuples.
    """
    if n is None:
        for line in fileStream:
            if line.startswith('#'):
                continue

            yield line.rstrip().split(separator)
    else:
        for line in fileStream:
            if line.startswith('#'):
                continue

            yield line.rstrip().split(separator, n)

    return

#----------------------------------------------------------------------------#

def intListPack(intList):
    """
    Packs a list of integers into a csv string.

        >>> intListPack([1, 2, 3, 7])
        '1-3,7'
    """
    if intList == []:
        # handle an empty list on packing and unpacking
        return ''

    intList.sort()

    packedElems = []

    startRange = lastInRange = intList[0]

    if startRange < 0:
        raise Exception, "Don't deal with negative numbers"

    i = 1
    intListLen = len(intList)
    while i < intListLen:
        while i < intListLen and intList[i] == lastInRange + 1:
            lastInRange += 1
            i += 1

        if lastInRange - startRange >= 1:
            # pack in short form
            packedElems.append('%d-%d' % (startRange, lastInRange))
        else:
            packedElems.append(str(startRange))

        if i == intListLen:
            break

        startRange = lastInRange = intList[i]
        i += 1
    else:
        packedElems.append(str(startRange))

    return ','.join(packedElems)

#----------------------------------------------------------------------------#

def intListUnpack(packedList):
    """
    Unpacks a packed integer list.

        >>> intListUnpack('1-3,7')
        [1, 2, 3, 7]
    """
    # handle an empty packed list
    if packedList == '':
        return []

    packedItems = packedList.split(',')

    unpackedElems = []
    for item in packedItems:
        if '-' in item:
            startRange, endRange = item.split('-')
            unpackedElems.extend(xrange(int(startRange), int(endRange)+1))
        else:
            unpackedElems.append(int(item))
    
    return unpackedElems

#----------------------------------------------------------------------------#

def flattenOnce(itemList):
    """
    Performs a single flatten on the given data list.

    @param itemList: The original data list.
    @return: A new list containing the same items, but with one level of
        list structure removed.
    """
    newItemList = []
    for item in itemList:
        if type(item) in (types.ListType, types.TupleType):
            newItemList.extend(item)
        else:
            newItemList.append(item)

    return newItemList

#----------------------------------------------------------------------------#

def groupByField(key, items, deleteField=False):
    """
    Performs a grouping of the items by key.
    """
    groups = {}
    for item in items:
        keyValue = item[key]
        if deleteField:
            del item[key]

        itemList = groups.setdefault(keyValue, [])
        itemList.append(item)
    
    return groups

#----------------------------------------------------------------------------#

def fieldHierarchy(fieldNames, recordList, deleteField=False):
    """
    The same as groupByField(), but it deletes the field key afterwards.
    """
    if len(fieldNames) == 1:
        # recursive base case
        return groupByField(fieldNames[0], recordList, deleteField)

    elif len(fieldNames) > 1:
        # group once then recurse for each key
        groupedFields = groupByField(fieldNames.pop(0), recordList,
                deleteField)
        for fieldKey in groupedFields.iterkeys():
            groupedFields[fieldKey] = fieldHierarchy(fieldNames,
                    groupedFields[fieldKey], deleteField)
        return groupedFields

    else:
        raise Exception, "Can't group by an empty path"

#----------------------------------------------------------------------------#
  
def tableToFields(headers, rows):
    """
    Restructures data between table form (a list of headers and rows) and
    field form (a list of key->value row dictionaries).
    """
    fieldRows = []

    for row in rows:
        fieldRows.append(dict(zip(headers, row)))
    
    return fieldRows

#----------------------------------------------------------------------------#

def fieldsToTable(fieldRows, order=None):
    """
    The reverse transformation to that performed by tableToFields(). If
    desired, the header fields can be given an order by specifying them in
    a list as the second argument. The number of table columns can be
    reduced by omitting some from the order list.
    """
    # first pass, accumulate unique keys
    headers = set()
    for fieldRow in fieldRows:
        for key in fieldRow.iterkeys():
            headers.add(key)

    # second pass, create table rows
    if order is None:
        headerList = list(headers)
    else:
        assert set(order).issubset(headers)
        headerList = order

    rows = []
    for fieldRow in fieldRows:
        row = []
        for key in headerList:
            row.append(fieldRow.get(key))
        rows.append(tuple(row))

    return headerList, rows

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

class CsvTable:
    """
    This class represents a generic data table, with row and column
    labels, and blocks which must be preserved.
    """

    #------------------------------------------------------------------------#

    def __init__(self, outputFile, columnsPerLine=20):
        """
        Constructor. Needs the labels for all the rows defined in a block.
        """
        self._blocks = []
        self._rowLabels = []

        self._currentWidth = 0

        self._colsPerLine = columnsPerLine

        self._lines = []
        self._oCsv = csv.writer(open(outputFile, 'w'))
        return

    #------------------------------------------------------------------------#

    def flush(self):
        """
        Flushes all blocks to the given csv file.
        """
        if not self._blocks:
            return

        headerRow = ['']
        subheaderRow = ['']
        for block in self._blocks:
            headerRow.extend(block.header())
            subheaderRow.extend(block.subheader())

        self._oCsv.writerow(headerRow)
        self._oCsv.writerow(subheaderRow)

        blockRows = map(
                flattenOnce, 
                apply( zip, [x.rows() for x in self._blocks] )
            )

        for rowLabel, row in zip(self._rowLabels, blockRows):
            self._oCsv.writerow([rowLabel] + row)

        self._oCsv.writerow([]) # add a black row between blocks

        # delete the blocks now that they've been printed
        self._blocks = []
        self._currentWidth = 0
        self._rowLabels = []

        return

    #------------------------------------------------------------------------#

    def addBlock(self, block):
        """
        Adds a block to the file, flushing out as necessary.
        """
        rowLabelsMatch = self._checkRowLabels(block.rowLabels())
        withinMaxCols = block.width() + self._currentWidth < self._colsPerLine

        if rowLabelsMatch and withinMaxCols:
            # all ok, within the maximum number of columns
            self._blocks.append(block)
            self._currentWidth += block.width()
        else:
            self.flush()

            # must fix labels before adding block
            self._checkRowLabels(block.rowLabels())

            # add the new block
            self._blocks = [block]
            self._currentWidth = block.width()

        return

    #------------------------------------------------------------------------#

    def _checkRowLabels(self, rowLabels):
        """
        Checks to ensure that the given row labels match the existing
        ones. In the case of an empty bock, adds the row labels in.
        Returns True if the labels match (or if the block was empty),
        False otherwise.

        @param rowLabels: The new block labels to check against the
            existing labels.
        @return: True if no flush is needed, False otherwise.
        """
        if self._blocks:
            # return True if the labels match
            return self._rowLabels == rowLabels
        else:
            # set the row labels to these ones
            self._rowLabels = rowLabels
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

    def __init__(self, blockLabel, rowLabels, columnLabels):
        self._rows = []

        self._blockLabel = blockLabel
        self._rowLabels = rowLabels
        self._columnLabels = columnLabels
        self._rowSize = None
        return

    #------------------------------------------------------------------------#

    def addRow(self, row):
        """
        Adds a row to the block.
        """
        rowLen = len(row)
        desiredSize = self._rowSize
        if desiredSize is not None and rowLen != desiredSize:
            raise Exception, "The added row is of the wrong size"

        self._rows.append(tuple(row))
        self._rowSize = rowLen
        return

    #------------------------------------------------------------------------#

    def width(self):
        """
        Returns the number of columns in the block.
        """
        return len(self._columnLabels)
    
    #------------------------------------------------------------------------#

    def height(self):
        """
        Determines the number of rows in the block.
        """
        return len(self._rowLabels)
    
    #------------------------------------------------------------------------#

    def rows(self):
        """
        Returns the rows for this block.
        """
        return self._rows

    #------------------------------------------------------------------------#

    def sameRowLabels(self, rhsBlock):
        """
        Determine if two blocks share row labels....
        """
        return self._rowLabels == rhsBlock._rowLabels

    #------------------------------------------------------------------------#

    def rowLabels(self):
        return self._rowLabels

    #------------------------------------------------------------------------#

    def header(self):
        """
        Returns the block header.
        """
        return [self._blockLabel] + [""]*(self.width()-1)

    #------------------------------------------------------------------------#

    def subheader(self):
        """
        Returns the block subheader.
        """
        return self._columnLabels

    #------------------------------------------------------------------------#

    def dump(self, outputFile):
        """
        Dumps this block to a csv file.
        """
        oCsv = csv.writer(open(outputFile, 'w'))
        oCsv.writerow(self.header())
        oCsv.writerow(self.subheader())
        for row in self._rows:
            oCsv.writerow(row)

        return

    #------------------------------------------------------------------------#

    def isEmpty(self):
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
