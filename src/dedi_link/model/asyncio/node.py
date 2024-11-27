from typing import TypeVar, Generic

from dedi_link.etc.exceptions import NodeNotImplemented
from .base_model import AsyncDataInterface
from ..data_index import DataIndexT
from ..user_mapping import UserMappingT
from ..node import NodeB


NodeT = TypeVar('NodeT', bound='Node')


class Node(NodeB[DataIndexT, UserMappingT],
           AsyncDataInterface,
           Generic[DataIndexT, UserMappingT]
           ):
    async def get_user_key(self, user_id: str) -> str:
        """
        Get the user key for the given user ID

        This key is usually stored in KMS or similar service,
        and should not be held in memory for long. This is why
        it's not stored as a property of the Node object.

        :param user_id: The user ID to get the key for
        :return: The user key
        """
        raise NodeNotImplemented('get_user_key method not implemented')
