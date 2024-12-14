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
    def __init__(self,
                 record_count: int = 0,
                 ):
        self.record_count = record_count

    def __bool__(self):
        return any([
            bool(self.record_count),
        ])

    def __eq__(self, other):
        if not isinstance(other, DataIndex):
            return NotImplemented

        return all([
            self.record_count == other.record_count,
        ])

    def __add__(self, other):
        if not isinstance(other, DataIndex):
            return NotImplemented

        return DataIndex(
            record_count=self.record_count + other.record_count,
        )

    def to_dict(self) -> dict:
        payload = {}

        if self.record_count:
            payload['recordCount'] = self.record_count

        return payload

    @classmethod
    def from_dict(cls: Type[DataIndexT], payload: dict) -> DataIndexT:
        return DataIndex(
            record_count=payload.get('recordCount', 0),
        )
