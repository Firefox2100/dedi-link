from typing import TypeVar

from dedi_link.etc.exceptions import NetworkNotImplemented
from .base_model import AsyncBaseModel
from .node import Node, NodeType
from ..data_index import DataIndexType
from ..network import Network as SyncNetwork


NetworkType = TypeVar('NetworkType', bound='Network')


class Network(AsyncBaseModel, SyncNetwork[DataIndexType, NodeType]):
    @property
    async def nodes(self) -> list[NodeType]:
        raise NetworkNotImplemented('nodes property not implemented')

    @property
    async def nodes_pending(self) -> list[NodeType]:
        raise NetworkNotImplemented('nodes_pending property not implemented')

    @property
    async def nodes_approved(self) -> list[NodeType]:
        raise NetworkNotImplemented('nodes_approved property not implemented')

    @property
    async def self_data_index(self) -> DataIndexType:
        raise NetworkNotImplemented('self_data_index property not implemented')

    @property
    async def network_data_index(self) -> DataIndexType:
        data_index = await self.self_data_index

        nodes = await self.nodes_approved

        for node in nodes:
            data_index += node.data_index

        return data_index