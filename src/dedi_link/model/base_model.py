from typing import Type, TypeVar

from dedi_link.etc.exceptions import BaseModelNotImplementedException


BaseModelType = TypeVar('BaseModelType', bound='BaseModel')


class BaseModel:
    """
    Abstract class for all models

    This class defines a uniform interface for all models to implement
    """
    @classmethod
    def load(cls: Type[BaseModelType], *args, **kwargs) -> BaseModelType:
        """
        Load a model from the database
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return: A single model instance
        """
        raise BaseModelNotImplementedException('load method has to be implemented by the child class')

    @classmethod
    def load_all(cls: Type[BaseModelType], *args, **kwargs) -> list[BaseModelType]:
        """
        Load all models from the database

        Most of the case, the parameters will not be used or provided; but in case a model needs
        to instruct on how to load, the parameters are kept
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return: A list of model instances
        """
        raise BaseModelNotImplementedException('load_all method has to be implemented by the child class')

    def store(self, *args, **kwargs):
        """
        Store the model in the database
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return:
        """
        raise BaseModelNotImplementedException('store method has to be implemented by the child class')

    def update(self, payload: dict):
        """
        Update the instance represented resource in the database

        This method should implement check for the payload to ensure unmutatable fields are not updated
        :param payload: The dictionary containing the new values
        :return: None
        """
        raise BaseModelNotImplementedException('update method has to be implemented by the child class')

    def delete(self, *args, **kwargs):
        """
        Delete the instance from the database
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return: None
        """
        raise BaseModelNotImplementedException('delete method has to be implemented by the child class')

    def to_dict(self) -> dict:
        """
        Serialize the instance to a dictionary
        :return: A dictionary representation of the instance
        """
        raise BaseModelNotImplementedException('to_dict method has to be implemented by the child class')

    @classmethod
    def from_dict(cls: Type[BaseModelType], payload: dict) -> BaseModelType:
        """
        Build an instance from a dictionary
        :param payload: The data dictionary containing the instance data
        :return: An instance of the model
        """
        raise BaseModelNotImplementedException('from_dict method has to be implemented by the child class')
