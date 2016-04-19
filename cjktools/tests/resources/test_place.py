# -*- coding: utf-8 -*-
#
#  test_place.py
#  cjktools
#
from __future__ import unicode_literals

import unittest
import os
import tempfile

from cjktools.resources import place


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(PlaceTestCase)
    ))
    return test_suite


class PlaceTestCase(unittest.TestCase):
    def setUp(self):
        self.melb = place.Place('Melbourne', 'メルボルン')
        self.aust = place.Place('Australia', 'オーストラリア')
        tmpfile, self.filename = tempfile.mkstemp()
        os.close(tmpfile)

    def test_basics(self):
        self.assertEqual(self.melb.label, 'Melbourne')
        self.assertEqual(self.melb.reading, 'メルボルン')

        self.aust.append(self.melb)

        self.assertIn(self.melb.label, self.aust)

    def test_formatting(self):
        original_place = self.aust
        melbourne = self.melb
        melbourne.append(place.Place('St_Kilda', 'セーントキルダ'))
        melbourne.append(place.Place('Collingwood', 'コーリングウード'))
        original_place.append(melbourne)

        sydney = place.Place('Sydney', 'シドニー')
        self.assertRaises(ValueError, place.Place, "Anja's place")

        sydney.append(place.Place("Anja's_place"))
        original_place.append(sydney)

        original_place.dump(self.filename)
        new_copy = place.Place.from_file(self.filename)
        self.assertEqual(new_copy, original_place)

    def tearDown(self):
        # Clean up the temp file we may have used.
        if os.path.exists(self.filename):
            os.remove(self.filename)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
