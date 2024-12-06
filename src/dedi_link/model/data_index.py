"""
A placeholder class for data index.
"""

from typing import TypeVar, Type

from .base_model import BaseModel


DataIndexT = TypeVar('DataIndexT', bound='DataIndex')


class DataIndex(BaseModel):
    """
    A placeholder class for data index.

    Extend it if your system stores or uses some type of
    index related to querying data.
    """
    def __init__(self):
        self.record_count = 0

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
    def from_dict(cls: Type[DataIndexT], payload: dict) -> DataIndexT:
        return DataIndex()
