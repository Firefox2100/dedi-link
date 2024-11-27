from typing import TypeVar, Generic

from dedi_link.etc.exceptions import NetworkNotImplemented
from .base_model import AsyncDataInterface
from .node import Node, NodeT
from ..data_index import DataIndexT
from ..network import NetworkB


NetworkT = TypeVar('NetworkT', bound='Network')


class Network(NetworkB[DataIndexT, NodeT],
              AsyncDataInterface,
              Generic[DataIndexT, NodeT]
              ):
    NODE_CLASS = Node

    @property
    async def nodes(self) -> list[NodeT]:
        raise NetworkNotImplemented('nodes property not implemented')

    @property
    async def nodes_pending(self) -> list[NodeT]:
        raise NetworkNotImplemented('nodes_pending property not implemented')

    @property
    async def nodes_approved(self) -> list[NodeT]:
        raise NetworkNotImplemented('nodes_approved property not implemented')

    @property
    async def self_data_index(self) -> DataIndexT:
        raise NetworkNotImplemented('self_data_index property not implemented')

    @property
    async def network_data_index(self) -> DataIndexT:
        data_index = await self.self_data_index

        nodes = await self.nodes_approved

        for node in nodes:
            data_index += node.data_index

        return data_index

    async def to_dict_with_index(self) -> dict:
        """
        Convert the network object to a dictionary, with index included.

        :return: Dictionary
        """
        data_index = await self.network_data_index

        payload = self.to_dict()

        payload['dataIndex'] = data_index.to_dict()

        return payload

    @property
    async def private_key(self) -> str:
        """
        Get the network private key.

        :return: Private key in PEM string format
        """
        raise NetworkNotImplemented('private_key property not implemented')
