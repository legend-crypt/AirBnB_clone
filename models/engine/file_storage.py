#!/usr/bin/python3
"""Module for FileStorage class"""


import contextlib
import json
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class for FileStorage"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f'{obj.__class__.__name__}.{obj.id}'
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        new_dict = {
            key: value.to_dict() for key, value in
            FileStorage.__objects.items()}
        with open(FileStorage.__file_path, mode='w', encoding='utf-8') as f:
            json.dump(new_dict, f, indent=4)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        with contextlib.suppress(FileNotFoundError):
            with open(FileStorage.__file_path, mode='r',
                      encoding='utf-8') as f:
                new_dict = json.load(f)
            for key, value in new_dict.items():
                class_name = value['__class__']
                del value['__class__']
                self.new(eval(class_name)(**value))

    def classes(self):
        """Returns a dictionary of valid classes"""
        return {
                "BaseModel": BaseModel,
                "User": User,
                "City": City,
                "Place": Place,
                "Amenity": Amenity,
                "State": State,
                "Review": Review
                }

    def attributes(self):
        """Returns a dictionary of valid attributes"""
        return {
                "BaseModel": ["id", "created_at", "updated_at"],
                "User": ["email", "password", "first_name", "last_name"],
                "City": ["state_id", "name"],
                "Place": ["city_id", "user_id", "name",
                          "description", "number_rooms",
                          "number_bathrooms", "max_guest",
                          "price_by_night",
                          "latitude", "longitude", "amenity_ids"],
                "Amenity": ["name"],
                "State": ["name"],
                "Review": ["place_id", "user_id", "text"]
                }
