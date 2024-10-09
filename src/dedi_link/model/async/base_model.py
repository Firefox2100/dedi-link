from typing import Type, TypeVar

from dedi_link.etc.exceptions import BaseModelNotImplementedException


AsyncBaseModelType = TypeVar('AsyncBaseModelType', bound='AsyncBaseModel')


class AsyncBaseModel:
    @classmethod
    async def load(cls: Type[AsyncBaseModelType], *args, **kwargs) -> AsyncBaseModelType:
        raise BaseModelNotImplementedException('load method has to be implemented by the child class')

    @classmethod
    async def load_all(cls: Type[AsyncBaseModelType], *args, **kwargs) -> list[AsyncBaseModelType]:
        raise BaseModelNotImplementedException('load_all method has to be implemented by the child class')

    async def store(self, *args, **kwargs):
        raise BaseModelNotImplementedException('store method has to be implemented by the child class')

    async def update(self, payload: dict):
        raise BaseModelNotImplementedException('update method has to be implemented by the child class')

    async def delete(self, *args, **kwargs):
        raise BaseModelNotImplementedException('delete method has to be implemented by the child class')

    def to_dict(self) -> dict:
        raise BaseModelNotImplementedException('to_dict method has to be implemented by the child class')

    @classmethod
    def from_dict(cls: Type[AsyncBaseModelType], payload: dict) -> AsyncBaseModelType:
        raise BaseModelNotImplementedException('from_dict method has to be implemented by the child class')
