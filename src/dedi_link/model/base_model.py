from enum import Enum
from typing import Type, TypeVar, Callable

from dedi_link.etc.exceptions import BaseModelNotImplemented


BaseModelType = TypeVar('BaseModelType', bound='BaseModel')


class BaseModel:
    """
    Abstract class for all models

    This class defines a uniform interface for all models to implement
    """
    @classmethod
    def _child_mapping(cls) -> dict[Enum, tuple[Type[BaseModelType], Callable[[dict], Enum] | None]]:
        """
        Mapping of the child classes to the enum values

        This is used to facilitate the factory method, and also allows for lazy
        importing within a method to avoid circular imports

        :return: A dictionary mapping the enum values to the child classes, and potentially a
        function to further identify the child class
        """
        return {}

    @classmethod
    def load(cls: Type[BaseModelType], *args, **kwargs) -> BaseModelType:
        """
        Load a model from the database
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return: A single model instance
        """
        raise BaseModelNotImplemented('load method has to be implemented by the child class')

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
        raise BaseModelNotImplemented('load_all method has to be implemented by the child class')

    def store(self, *args, **kwargs):
        """
        Store the model in the database
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return:
        """
        raise BaseModelNotImplemented('store method has to be implemented by the child class')

    def update(self, payload: dict):
        """
        Update the instance represented resource in the database

        This method should implement check for the payload to ensure unmutatable fields are not updated
        :param payload: The dictionary containing the new values
        :return: None
        """
        raise BaseModelNotImplemented('update method has to be implemented by the child class')

    def delete(self, *args, **kwargs):
        """
        Delete the instance from the database
        :param args: Unnamed arguments
        :param kwargs: Named arguments
        :return: None
        """
        raise BaseModelNotImplemented('delete method has to be implemented by the child class')

    def to_dict(self) -> dict:
        """
        Serialize the instance to a dictionary
        :return: A dictionary representation of the instance
        """
        raise BaseModelNotImplemented('to_dict method has to be implemented by the child class')

    @classmethod
    def from_dict(cls: Type[BaseModelType], payload: dict) -> BaseModelType:
        """
        Build an instance from a dictionary
        :param payload: The data dictionary containing the instance data
        :return: An instance of the model
        """
        raise BaseModelNotImplemented('from_dict method has to be implemented by the child class')

    @classmethod
    def factory(cls: Type[BaseModelType], payload: dict, id_var: Enum):
        """
        Create an instance of (usually) a child class from a dictionary,
        by following the mapping defined as a class attribute
        :param payload:
        :param id_var:
        :return:
        """
        if not cls._child_mapping():
            # No known mapping, just create the class itself
            return cls.from_dict(payload)

        if id_var not in cls._child_mapping():
            raise ValueError(f'{id_var} not found in the defined mapping')

        mapping_target = cls._child_mapping()[id_var]

        if mapping_target[1] is None:
            # Basic mapping, create the object by calling the from_dict method
            return mapping_target[0].from_dict(payload)
        else:
            # A deeper mapping function provided, get the new id_var and call factory again
            new_id_var = mapping_target[1](payload)
            return mapping_target[0].factory(payload, new_id_var)
