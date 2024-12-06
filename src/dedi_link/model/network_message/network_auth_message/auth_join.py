import uuid
from typing import TypeVar, Generic, Type

from dedi_link.etc.consts import MESSAGE_DATA, MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import AuthMessageType
from ...node import Node, NodeT
from ...network import NetworkT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ..network_message_header import NetworkMessageHeaderT
from .network_auth_message import NetworkAuthMessageB, NetworkAuthMessage


AuthJoinBT = TypeVar('AuthJoinBT', bound='AuthJoinB')
AuthJoinT = TypeVar('AuthJoinT', bound='AuthJoin')


class AuthJoinB(NetworkAuthMessageB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                ):
    NODE_CLASS = Node[DataIndexT, UserMappingT]

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 node: NodeT,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Base class for Network Authorization Join Message

        :param network_id: The network ID
        :param node_id: The node ID
        :param node: The node that is joining
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            network_id=network_id,
            node_id=node_id,
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
            'node': self.node.to_dict(key=True),
        }

        return payload

    @classmethod
    def from_dict(cls: Type[AuthJoinBT], payload: dict) -> AuthJoinBT:
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            timestamp=payload['timestamp'],
            node=cls.NODE_CLASS.from_dict(payload[MESSAGE_DATA]['node']),
        )


class AuthJoin(AuthJoinB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
               NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
               Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
               ):
    """
    Network Authorization Join Message

    This message notifies the other nodes within the network about
    a new node joining. The node information is only for the others
    to record it initially, and they will synchronise with the new
    node directly.
    """
