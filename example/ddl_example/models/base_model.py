from dedi_link.model import BaseModel as BaseModelLib, SyncDataInterface

from .database import InMemoryDatabase


class BaseModel(BaseModelLib, SyncDataInterface):
    db = InMemoryDatabase()

    @property
    def access_token(self) -> str:
        """
        Get the access token for the model

        This is a property to allow for lazy loading of the access token
        :return: The access token
        """
        raise NotImplementedError(
            'access_token property has to be implemented by the child class'
        )
