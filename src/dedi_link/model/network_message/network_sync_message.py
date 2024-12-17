"""
Network Synchronisation Message
"""

from typing import TypeVar, Generic, Type
from deepdiff import DeepDiff

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES, MESSAGE_DATA
from dedi_link.etc.enums import SyncTarget, MessageType
from ..network import NetworkT
from ..node import Node, NodeT
from ..data_index import DataIndexT
from ..user_mapping import UserMappingT
from .network_message import NetworkMessageBase, NetworkMessage
from .network_message_header import NetworkMessageHeaderT


NetworkSyncMessageBaseT = TypeVar('NetworkSyncMessageBaseT', bound='NetworkSyncMessageBase')
NetworkSyncMessageT = TypeVar('NetworkSyncMessageT', bound='NetworkSyncMessage')


class NetworkSyncMessageBase(NetworkMessageBase[
                                 NetworkMessageHeaderT,
                                 NetworkT,
                                 DataIndexT,
                                 UserMappingT,
                                 NodeT
                             ],
                             Generic[
                                 NetworkMessageHeaderT,
                                 NetworkT,
                                 DataIndexT,
                                 UserMappingT,
                                 NodeT
                             ]):
    """
    Base class for Network Synchronisation Messages
    """
    NODE_CLASS = Node[DataIndexT, UserMappingT]
    message_type = MessageType.SYNC_MESSAGE

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 target_type: SyncTarget,
                 data: list[dict | NetworkT | NodeT] | None = None,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Network Synchronisation Message

        These messages are used to synchronise the state of nodes within a network.

        :param network_id: The network ID
        :param node_id: The node ID
        :param target_type: The target type of the sync
        :param data: The data to synchronise
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            message_id=message_id,
            timestamp=timestamp,
        )

        self.target_type = target_type
        self.data = data

    def __eq__(self, other):
        if not isinstance(other, NetworkSyncMessageBase):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.target_type == other.target_type,
            not bool(DeepDiff(
                self.data,
                other.data,
                ignore_order=True,
            )),
        ])

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.target_type,
        ))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES].update({
            'targetType': self.target_type.value,
        })

        if self.data is not None:
            message_data = []

            for data_item in self.data:
                if isinstance(data_item, dict):
                    message_data.append(data_item)
                elif isinstance(data_item, Node):
                    message_data.append(data_item.to_dict(key=True))
                else:
                    message_data.append(data_item.to_dict())

            payload[MESSAGE_DATA] = message_data

        return payload

    @classmethod
    def from_dict(cls: Type[NetworkSyncMessageBaseT], payload: dict) -> NetworkSyncMessageBaseT:
        if MESSAGE_DATA in payload:
            message_data = []

            for data_item in payload[MESSAGE_DATA]:
                if 'nodeId' in data_item:
                    message_data.append(cls.NODE_CLASS.from_dict(data_item))
                elif 'networkId' in data_item:
                    message_data.append(cls.NETWORK_CLASS.from_dict(data_item))
                else:
                    message_data.append(data_item)
        else:
            message_data = None

        return cls(
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            target_type=SyncTarget(payload[MESSAGE_ATTRIBUTES]['targetType']),
            data=message_data,
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            timestamp=payload['timestamp'],
        )


class NetworkSyncMessage(NetworkSyncMessageBase[
                             NetworkMessageHeaderT,
                             NetworkT,
                             DataIndexT,
                             UserMappingT,
                             NodeT
                         ],
                         NetworkMessage[
                             NetworkMessageHeaderT,
                             NetworkT,
                             DataIndexT,
                             UserMappingT,
                             NodeT
                         ],
                         Generic[
                             NetworkMessageHeaderT,
                             NetworkT,
                             DataIndexT,
                             UserMappingT,
                             NodeT
                         ]):
    """
    Network Synchronisation Message

    These messages are used to synchronise the state of nodes within a network.
    """
