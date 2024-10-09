from typing import TypeVar

from .base_model import BaseModel


UserMappingType = TypeVar('UserMappingType', bound='UserMapping')


class UserMapping(BaseModel):
    pass
