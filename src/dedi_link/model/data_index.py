from typing import TypeVar

from .base_model import BaseModel


DataIndexType = TypeVar('DataIndexType', bound='DataIndex')


class DataIndex(BaseModel):
    pass
