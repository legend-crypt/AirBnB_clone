#!/usr/bin/env python3

"""
    model for review class
"""


from models.base_model import BaseModel


class Review(BaseModel):
    """
        class for review of the place
    """
    place_id = ""
    user_id = ""
    text = ""
