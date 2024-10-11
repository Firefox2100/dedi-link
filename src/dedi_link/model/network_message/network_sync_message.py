import uuid
from deepdiff import DeepDiff
from typing import TypeVar

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES, MESSAGE_DATA
from dedi_link.etc.enums import SyncTarget, MessageType
from .network_message import NetworkMessage


NetworkSyncMessageType = TypeVar('NetworkSyncMessageType', bound='NetworkSyncMessage')


class NetworkSyncMessage(NetworkMessage):
    """
    Network Synchronization Message

    These messages are used to synchronize the state of nodes within a network.
    """
    def __init__(self,
                 node_id: str,
                 target_type: SyncTarget,
                 data: list | None = None,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        super().__init__(
            message_type=MessageType.SYNC_MESSAGE,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.node_id = node_id
        self.target_type = target_type
        self.data = data

    def __eq__(self, other: 'NetworkSyncMessage'):
        if not isinstance(other, NetworkSyncMessage):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.node_id == other.node_id,
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
            self.node_id,
            self.target_type,
        ))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES].update({
            'messageID': self.message_id,
            'nodeID': self.node_id,
            'targetType': self.target_type.value,
        })

        if self.data is not None:
            payload[MESSAGE_DATA] = self.data

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> 'NetworkSyncMessage':
        return cls(
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeID'],
            target_type=SyncTarget(payload[MESSAGE_ATTRIBUTES]['targetType']),
            data=payload.get(MESSAGE_DATA, None),
            message_id=payload[MESSAGE_ATTRIBUTES]['messageID'],
            timestamp=payload['timestamp'],
        )
