# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------#
# xmlTools.py
# vim: ts=4 sw=4 sts=4 et tw=78:
# Mon Oct 16 13:20:06 2006
#
#----------------------------------------------------------------------------#

"""
Some XML helper methods, and an interface for accessing a large XML document
in parts, without loading it all into memory at once.
"""

#----------------------------------------------------------------------------#

import enum, common

import os, re
import cPickle as pickle
from xml.dom import minidom
from xml.xpath import Evaluate

#----------------------------------------------------------------------------#
# PUBLIC
#----------------------------------------------------------------------------#

def EvaluateLeaf(expr, node, typecast=None, maybeEmpty=False):
    """
    Get the text for the unique result of this expression. If more than
    one value results, an exception is thrown. Essentially

    @param expr: The xpath expression to execute.
    @param node: The node to execute the expression over.
    @param typecast: An optional function to apply to values before
        returning them.
    @param maybeEmpty: If True, will return None instead of raising an
        exception if no value is found.
    """
    childNodes = Evaluate(expr, node)

    if len(childNodes) == 1:
        # Normal case, a unique value.
        childNode = childNodes[0]
        return _nodeValue(childNode, typecast)

    elif len(childNodes) == 0 and maybeEmpty:
        # We might allow a missing value.
        return None

    else:
        # Too many values!
        raise Exception, "A unique value was expected"

#----------------------------------------------------------------------------#

def EvaluateLeaves(expr, node, typecast=None):
    """
    Get the data from the results of the expression, returned as a tuple of
    all matches.
    """
    nodes = Evaluate(expr, node)

    results = []
    for childNode in nodes:
        results.append(_nodeValue(childNode, typecast))

    return tuple(results)

#----------------------------------------------------------------------------#
#----------------------------------------------------------------------------#

IndexType = enum.Enum('attribute', 'element')

#----------------------------------------------------------------------------#

class IndexedDocument(object):
    """
    A document with an inverted index stored in memory, permitting rapid
    access to elements of the XML document as required. Uses regular
    expressions rather than XML libraries on the initial parse, making it
    considerably faster and less resource intensive.
    """

    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, filename, baseTag, keyPath):
        """
        Constructor. Takes the given document, and reads in the index for
        that document. If no index exists, then one is created. The
        tagSpec gives the path that should be indexed.
        
        For example, a tagSpec of 'kanji.midashi' indicates that <kanji>
        entries should be indexed, using the contents of the <midashi>
        sub-element as a key.  A tagSpec of 'strokegr:element' indicates
        that <strokegr> entries should be indexed via their element
        attribute.

        @param filename: The document to access via index.
        @param baseTag: The elements to index.
        @param keyPath: The path from within a base tag to use for an
            indexing key.
        """
        self._fileStream = common.sopen(filename, encoding=None)
        self._baseTag = baseTag
        self._keyPath = keyPath
        self._xmlHeader = '<?xml version="1.0" encoding="UTF-8"?>'

        indexFile = '%s.index' % filename
        if os.path.exists(indexFile):
            self._index = pickle.load(open(indexFile, 'r'))
        else:
            self._index = self._generateIndex(filename)
            oStream = open(indexFile, 'w')
            pickle.dump(self._index, oStream)
            oStream.close()

        return

    #------------------------------------------------------------------------#

    def keys(self):
        """
        Returns a list of indexed keys.

        @return: All available keys.
        """
        return self._index.keys()

    #------------------------------------------------------------------------#

    def itervalues(self, unlink=True):
        """
        Iterates over the XML values in this document. Note that each node
        is automatically unlinked before the next is made available,
        unless the unlink flag is made False.
        """
        for key in self.keys():
            value = self[key]
            yield value
            if unlink:
                value.unlink()

        return

    #------------------------------------------------------------------------#

    def __getitem__(self, key):
        """
        Returns an xml document node for the given key. Note that the node
        should be unlinked after use, by calling its node.unlink() method,
        so that it can be garbage collected accurately.

        @param key: The key to look-up.
        @return: An xml document node for the entry that was found.
        """
        startRange, endRange = self._index[key]
        self._fileStream.seek(startRange)
        data = self._fileStream.read(endRange - startRange)
        doc = minidom.parseString(self._xmlHeader + data)
        return doc

    #------------------------------------------------------------------------#

    def __len__(self):
        """
        Return the number of entries indexed.
        """
        return len(self._index)

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#

    def _generateIndex(self, filename):
        """
        Generates a new index file, using the tagPath and indexType to
        determine what should be indexed and what key should be used.

        @param filename: The file to index.
        @return: A dictionary mapping key to xml snippet.
        """
        index = {}

        data = common.sopen(filename, encoding=None).read()
        tagPattern = re.compile(
                '<%s[^>]*>.*?</%s>' % (self._baseTag, self._baseTag),
                re.UNICODE | re.MULTILINE | re.DOTALL,
            )

        for match in tagPattern.finditer(data):
            # Create a small XML document containing just this tag's data.
            xmlData = match.group()
            doc = minidom.parseString(self._xmlHeader + xmlData)

            # Fetch the key to index this section by.
            keyValue = EvaluateLeaf(self._baseTag + '/' + self._keyPath, doc)

            # Reclaim the memory.
            doc.unlink()

            # Store the location of this entry for later.
            index[keyValue] = match.span()

        return index
    
    #------------------------------------------------------------------------#

    def _determineTagPath(self, tagSpec):
        """
        Determine the tag path and type of spec from the tag spec given.
        Return both as a tuple.

        @param tagSpec: The index tag specification.  
        @return: (tagPath, indexType) where the tagPath is a flat list of
            element tags, optionally with an attribute name at the end.
        """
        tagPath = tagSpec.split('.')
        if ':' in tagPath[-1]:
            tagPath.extend(tagPath.pop().split(':')[:2])
            indexType = IndexType.attribute
        else:
            indexType = IndexType.element

        return tagPath, indexType

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# PRIVATE
#----------------------------------------------------------------------------#

def _nodeValue(node, typecast=None):
    """
    Fetch the actual value of this node, which must be a leaf node.
    """
    text = []
    for child in node.childNodes:
        if child.nodeType != child.TEXT_NODE:
            raise Exception, "Tried to evaluate a non-leaf node"

        text.append(child.nodeValue)

    result = ''.join(text)

    if typecast is not None:
        result = typecast(result)

    return result

#----------------------------------------------------------------------------#
