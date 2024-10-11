import uuid
from typing import TypeVar, Type, Generic

from dedi_link.etc.consts import MESSAGE_DATA, MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import AuthMessageType
from ...node import Node, NodeType
from .network_auth_message import NetworkAuthMessage


AuthJoinType = TypeVar('AuthJoinType', bound='AuthJoin')


class AuthJoin(NetworkAuthMessage, Generic[NodeType]):
    """
    Network Authorization Join Message

    This message notifies the other nodes within the network about
    a new node joining. The node information is only for the others
    to record it initially, and they will synchronise with the new
    node directly.
    """
    NODE_CLASS = Node

    def __init__(self,
                 network_id: str,
                 node: NodeType,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        super().__init__(
            network_id=network_id,
            auth_type=AuthMessageType.JOIN,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.node = node

    def __eq__(self, other: 'AuthJoin'):
        if not isinstance(other, AuthJoin):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.node == other.node,
        ])

    def __hash__(self):
        return hash((super().__hash__(), self.node))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_DATA] = {
            'node': self.node.to_dict(key=True)
        }

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> 'AuthJoin':
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageID'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkID'],
            timestamp=payload['timestamp'],
            node=cls.NODE_CLASS.from_dict(payload[MESSAGE_DATA]['node']),
        )
