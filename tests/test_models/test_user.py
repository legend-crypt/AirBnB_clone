#!/usr/bin/python3
""" unittest for user class model"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models import storage
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the User class."""

    def test_no_args_instantiates(self):
        self.assertEqual(User, type(User()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(User(), storage.all().values())

    def test_id_is_public_str(self):
        self.assertIsInstance(User().id, str)

    def test_created_at_is_public_datetime(self):
        self.assertIsInstance(User().created_at, datetime)

    def test_updated_at_is_public_datetime(self):
        self.assertIsInstance(User().updated_at, datetime)

    def test_email_is_public_str(self):
        self.assertIsInstance(User.email, str)

    def test_password_is_public_str(self):
        self.assertIsInstance(User.password, str)

    def test_first_name_is_public_str(self):
        self.assertIsInstance(User.first_name, str)

    def test_last_name_is_public_str(self):
        self.assertIsInstance(User.last_name, str)

    def test_two_users_unique_ids(self):
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)

    def test_two_users_different_created_at(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.created_at, user2.created_at)

    def test_two_users_different_updated_at(self):
        user1 = User()
        sleep(0.05)
        user2 = User()
        self.assertLess(user1.updated_at, user2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        user = User()
        user.id = "123456"
        user.created_at = user.updated_at = dt
        user_str = user.__str__()
        self.assertIn("[User] (123456)", user_str)
        self.assertIn("'id': '123456'", user_str)
        self.assertIn("'created_at': " + dt_repr, user_str)
        self.assertIn("'updated_at': " + dt_repr, user_str)

    def test_args_unused(self):
        user = User(None)
        self.assertNotIn(None, user.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        user = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, dt)
        self.assertEqual(user.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Unittests for testing save method of the User class."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except OSError:
            pass

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except OSError:
            pass
        try:
            os.rename("tmp", "file.json")
        except OSError:
            pass

    def test_one_save(self):
        user = User()
        sleep(0.05)
        first_updated_at = user.updated_at
        user.save()
        self.assertLess(first_updated_at, user.updated_at)

    def test_save_updates_file(self):
        user = User()
        user.save()
        user_id = "User." + user.id
        with open("file.json", "r") as f:
            self.assertIn(user_id, f.read())


if __name__ == "__main__":
    unittest.main()
