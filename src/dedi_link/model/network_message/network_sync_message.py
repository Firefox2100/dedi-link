from deepdiff import DeepDiff
from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES, MESSAGE_DATA
from dedi_link.etc.enums import SyncTarget, MessageType
from ..network import NetworkT
from ..node import Node, NodeT
from .network_message import NetworkMessage
from .network_message_header import NetworkMessageHeaderT


NetworkSyncMessageT = TypeVar('NetworkSyncMessageT', bound='NetworkSyncMessage')


class NetworkSyncMessage(NetworkMessage[NetworkMessageHeaderT, NetworkT],
                         Generic[NetworkMessageHeaderT, NetworkT, NodeT],
                         ):
    NODE_CLASS = Node

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 target_type: SyncTarget,
                 data: list[dict | NetworkT | NodeT] | None = None,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Network Synchronization Message

        These messages are used to synchronise the state of nodes within a network.

        :param network_id: The network ID
        :param node_id: The node ID
        :param target_type: The target type of the sync
        :param data: The data to synchronise
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            message_type=MessageType.SYNC_MESSAGE,
            network_id=network_id,
            node_id=node_id,
            message_id=message_id,
            timestamp=timestamp,
        )

        self.target_type = target_type
        self.data = data

    def __eq__(self, other: 'NetworkSyncMessage'):
        if not isinstance(other, NetworkSyncMessage):
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
                elif isinstance(data_item, self.NODE_CLASS):
                    message_data.append(data_item.to_dict(key=True))
                else:
                    message_data.append(data_item.to_dict())

            payload[MESSAGE_DATA] = message_data

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> 'NetworkSyncMessage':
        if MESSAGE_DATA in payload:
            message_data = []

            for data_item in payload[MESSAGE_DATA]:
                if 'nodeId' in data_item:
                    message_data.append(cls.NODE_CLASS.from_dict(data_item))
                elif 'networkId' in data_item:
                    message_data.append(NetworkT.from_dict(data_item))
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
