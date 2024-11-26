from typing import TypeVar

from .base_model import AsyncBaseModel
from ..user import User as SyncUser


UserT = TypeVar('UserT', bound='User')


class User(SyncUser, AsyncBaseModel):
    pass
