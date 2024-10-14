from typing import TypeVar

from .base_model import BaseModel


DataIndexType = TypeVar('DataIndexType', bound='DataIndex')


class DataIndex(BaseModel):
    def __add__(self, other):
        if not isinstance(other, DataIndex):
            return NotImplemented

        return DataIndex()
