#!/usr/bin/python3
import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    def test_init_with_arguments(self):
        """Test initialization of base_model with arguments"""
        id_val = "123"
        created_at_val = "2022-01-01T00:00:00.000000"
        updated_at_val = "2022-01-01T01:00:00.000000"
        kwargs = {
                "id": id_val,
                "created_at": created_at_val,
                "updated_at": updated_at_val,
                "custom_attr": "test",
                }
        model = BaseModel(**kwargs)
        self.assertEqual(model.id, id_val)
        self.assertEqual(model.created_at,
                         datetime.strptime(created_at_val,
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(model.updated_at,
                         datetime.strptime(updated_at_val,
                                           "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertEqual(model.custom_attr, "test")

    def test_init_without_arguments(self):
        """Test initialization of base_model without arguments"""
        model = BaseModel()
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_str(self):
        """Test string representation of base_model"""
        model = BaseModel()
        string = f"[{model.__class__.__name__}] ({model.id}) {model.__dict__}"
        self.assertEqual(str(model), string)

    def test_save(self):
        """Test save method of base_model"""
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()
        self.assertNotEqual(old_updated_at, model.updated_at)

    def test_to_dict(self):
        """Test to_dict method of base_model"""
        model = BaseModel()
        new_dict = model.to_dict()
        self.assertIsInstance(new_dict, dict)
        self.assertEqual(new_dict['__class__'], 'BaseModel')
        self.assertEqual(new_dict['id'], model.id)
        self.assertEqual(new_dict['created_at'], model.created_at.isoformat())
        self.assertEqual(new_dict['updated_at'], model.updated_at.isoformat())


if __name__ == '__main__':
    unittest.main()
