# -*- coding: utf-8 -*-
#
#  test_place.py
#  cjktools
#


import unittest
import os

import warnings
warnings.simplefilter("ignore", RuntimeWarning)

import place


def suite():
    test_suite = unittest.TestSuite((
        unittest.makeSuite(PlaceTestCase)
    ))
    return test_suite


class PlaceTestCase(unittest.TestCase):
    def setUp(self):
        self.melb = place.Place(u'Melbourne', u'メルボルン')
        self.aust = place.Place(u'Australia', u'オーストラリア')
        self.filename = os.tmpnam()

    def test_basics(self):
        self.assertEqual(self.melb.label, u'Melbourne')
        self.assertEqual(self.melb.reading, u'メルボルン')

        self.aust.append(self.melb)

        assert self.melb.label in self.aust
        return

    def test_formatting(self):
        original_place = self.aust
        melbourne = self.melb
        melbourne.append(place.Place('St_Kilda', u'セーントキルダ'))
        melbourne.append(place.Place('Collingwood', u'コーリングウード'))
        original_place.append(melbourne)
        sydney = place.Place('Sydney', u'シドニー')
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
        return


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
