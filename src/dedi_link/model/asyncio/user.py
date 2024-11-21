from typing import TypeVar

from .base_model import AsyncBaseModel
from ..user import User as SyncUser


UserType = TypeVar('UserType', bound='User')


class User(AsyncBaseModel, SyncUser):
    pass
