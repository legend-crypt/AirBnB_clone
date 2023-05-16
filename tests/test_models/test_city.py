#!/usr/bin/env python3
"""Unittest model for the city class"""

import unittest
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):
    def test_attributes(self):
        """Test initialization of City attributes"""
        city = City()
        self.assertEqual(city.state_id, "")
        self.assertEqual(city.name, "")

    def test_inheritance(self):
        """Test if City inherits from BaseModel"""
        city = City()
        self.assertIsInstance(city, BaseModel)

    def test_str_representation(self):
        """Test string representation of City"""
        city = City()
        string = f"[{city.__class__.__name__}] ({city.id}) {city.__dict__}"
        self.assertEqual(str(city), string)


if __name__ == '__main__':
    unittest.main()
