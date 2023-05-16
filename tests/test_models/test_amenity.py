#!/usr/bin/python3
"""Defines unittests for models/amenity.py"""
import unittest
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    def test_attributes(self):
        amenity = Amenity()
        self.assertEqual(amenity.name, "")

    def test_str_representation(self):
        amenity = Amenity()
        amenity.name = "Wifi"
        expected = "[Amenity] ({})".format(amenity.id)
        self.assertEqual(str(amenity)[:len(expected)], expected)

    def test_to_dict_method(self):
        amenity = Amenity()
        amenity.name = "Wifi"
        amenity_dict = amenity.to_dict()
        self.assertEqual(amenity_dict["name"], "Wifi")
        self.assertEqual(amenity_dict["__class__"], "Amenity")
        self.assertTrue("__class__" in amenity_dict)
        self.assertTrue("created_at" in amenity_dict)
        self.assertTrue("updated_at" in amenity_dict)
        self.assertTrue("id" in amenity_dict)


if __name__ == '__main__':
    unittest.main()
