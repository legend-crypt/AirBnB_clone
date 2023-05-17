#!/usr/bin/env python3

"""
    model for the city class
"""

from models.base_model import BaseModel


class City(BaseModel):
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):

        """class constructor"""
        super().__init__(*args, **kwargs)
