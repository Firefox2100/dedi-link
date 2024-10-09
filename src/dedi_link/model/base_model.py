from typing import Type, TypeVar

from dedi_link.etc.exceptions import BaseModelNotImplementedException


BaseModelType = TypeVar('BaseModelType', bound='BaseModel')


class BaseModel:
    @classmethod
    def load(cls: Type[BaseModelType], *args, **kwargs) -> BaseModelType:
        raise BaseModelNotImplementedException('load method has to be implemented by the child class')

    @classmethod
    def load_all(cls: Type[BaseModelType], *args, **kwargs) -> list[BaseModelType]:
        raise BaseModelNotImplementedException('load_all method has to be implemented by the child class')

    def store(self, *args, **kwargs):
        raise BaseModelNotImplementedException('store method has to be implemented by the child class')

    def update(self, payload: dict):
        raise BaseModelNotImplementedException('update method has to be implemented by the child class')

    def delete(self, *args, **kwargs):
        raise BaseModelNotImplementedException('delete method has to be implemented by the child class')

    def to_dict(self) -> dict:
        raise BaseModelNotImplementedException('to_dict method has to be implemented by the child class')

    @classmethod
    def from_dict(cls: Type[BaseModelType], payload: dict) -> BaseModelType:
        raise BaseModelNotImplementedException('from_dict method has to be implemented by the child class')
