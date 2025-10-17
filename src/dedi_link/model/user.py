"""
A module defining the User model.
"""


from uuid import uuid4
from pydantic import Field, ConfigDict

from .base import JsonModel


class User(JsonModel):
    """
    A class representing a user in the system.
    """

    model_config = ConfigDict(
        serialize_by_alias=True,
        validate_by_name=True,
        validate_by_alias=True,
    )

    user_id: str = Field(
        default_factory=lambda: str(uuid4()),
        alias='userId',
        description='Unique user ID (UUID4)'
    )
