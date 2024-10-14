from typing import Type, TypeVar

from dedi_link.etc.exceptions import BaseModelNotImplemented
from ..base_model import BaseModel


AsyncBaseModelType = TypeVar('AsyncBaseModelType', bound='AsyncBaseModel')


class AsyncBaseModel(BaseModel):
    """
    Asynchronous base class for the async part of library
    """
    @classmethod
    async def load(cls: Type[AsyncBaseModelType], *args, **kwargs) -> AsyncBaseModelType:
        """
        Load a model from the database asynchronously
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return: A single model instance
        """
        raise BaseModelNotImplemented('load method has to be implemented by the child class')

    @classmethod
    async def load_all(cls: Type[AsyncBaseModelType], *args, **kwargs) -> list[AsyncBaseModelType]:
        """
        Load all models from the database asynchronously

        Most of the case, the parameters will not be used or provided; but in case a model needs
        to instruct on how to load, the parameters are kept
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return: A list of model instances
        """
        raise BaseModelNotImplemented('load_all method has to be implemented by the child class')

    async def store(self, *args, **kwargs):
        """
        Store the model in the database asynchronously
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return:
        """
        raise BaseModelNotImplemented('store method has to be implemented by the child class')

    async def update(self, payload: dict):
        """
        Update the instance represented resource in the database asynchronously

        This method should implement check for the payload to ensure unmutatable fields are not updated
        :param payload: The dictionary containing the new values
        :return: None
        """
        raise BaseModelNotImplemented('update method has to be implemented by the child class')

    async def delete(self, *args, **kwargs):
        """
        Delete the instance from the database asynchronously
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return: None
        """
        raise BaseModelNotImplemented('delete method has to be implemented by the child class')