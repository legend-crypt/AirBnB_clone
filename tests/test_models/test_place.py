#!/usr/bin/env python3
"""unittest for the place class"""

import unittest
from models.place import Place
from models.base_model import BaseModel


class TestPlace(unittest.TestCase):
    def test_attributes(self):
        """Test initialization of Place attributes"""
        place = Place()
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.description, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.amenity_ids, "")

    def test_inheritance(self):
        """Test if Place inherits from BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)

    def test_str_representation(self):
        """Test string representation of Place"""
        place = Place()
        string = f"[{place.__class__.__name__}] ({place.id}) {place.__dict__}"
        self.assertEqual(str(place), string)


if __name__ == '__main__':
    unittest.main()
