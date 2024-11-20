from typing import TypeVar

from .base_model import BaseModel


DataIndexType = TypeVar('DataIndexType', bound='DataIndex')


class DataIndex(BaseModel):
    def __eq__(self, other):
        if not isinstance(other, DataIndex):
            return NotImplemented

        return True

    def __add__(self, other):
        if not isinstance(other, DataIndex):
            return NotImplemented

        return DataIndex()

    def to_dict(self) -> dict:
        return {}

    @classmethod
    def from_dict(cls, payload: dict) -> 'DataIndex':
        return DataIndex()
