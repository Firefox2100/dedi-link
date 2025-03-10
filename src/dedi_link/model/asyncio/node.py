from typing import TypeVar, Generic

from dedi_link.etc.exceptions import NodeNotImplemented
from .base_model import AsyncDataInterface
from ..data_index import DataIndexT
from ..user_mapping import UserMappingT
from ..node import NodeBase


NodeT = TypeVar('NodeT', bound='Node')


class Node(NodeBase[DataIndexT, UserMappingT],
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

    async def store_user_key(self, user_id: str, user_key: str):
        """
        Store the user key for the given user ID

        This key is usually stored in KMS or similar service,
        and should not be held in memory for long. This is why
        it's not stored as a property of the Node object.

        :param user_id: The user ID to store the key for
        :param user_key: The user key to store
        """
        raise NodeNotImplemented('store_user_key method not implemented')

    async def update_score(self,
                     score: float,
                     ):
        """
        Wrapper method to update only the score of a node

        The score is updated with each request, so this method is
        more convenient to use than the update() method.

        :param score: New score to set
        :return:
        """
        new_score = self._ema_score(score)

        await self.update({
            'score': new_score,
        })
