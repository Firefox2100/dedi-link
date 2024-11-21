import uuid
from deepdiff import DeepDiff
from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES, MESSAGE_DATA
from dedi_link.etc.enums import AuthMessageType, AuthMessageStatus
from ...node import Node, NodeType
from ...network import Network, NetworkType
from .network_auth_message import NetworkAuthMessage


AuthRequestInviteType = TypeVar('AuthRequestInviteType', bound='AuthRequestInvite')


class AuthRequestInvite(NetworkAuthMessage, Generic[NodeType, NetworkType]):
    """
    Network Authorization Request or Invite Message

    This message is for requesting to join a network by asking a node,
    or to invite a node to join a network that this node is in.
    """
    NODE_CLASS = Node
    NETWORK_CLASS = Network

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 auth_type: AuthMessageType,
                 status: AuthMessageStatus,
                 node: NodeType,
                 target_url: str,
                 challenge: list[str],
                 message_id: str = None,
                 timestamp: int | None = None,
                 network: NetworkType | None = None,
                 ):
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            auth_type=auth_type,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.status = status
        self.target_url = target_url
        self.node = node
        self.challenge = challenge
        self.network = network

        if network is not None:
            assert self.network_id == self.network.network_id

    def __eq__(self, other: 'AuthRequestInvite'):
        if not isinstance(other, self.__class__):
            return NotImplemented

        if DeepDiff(
            self.challenge,
            other.challenge,
            ignore_order=True,
        ):
            return False

        return all([
            super().__eq__(other),
            self.status == other.status,
            self.target_url == other.target_url,
            self.node == other.node,
            self.network == other.network,
        ])

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.status,
            self.target_url,
            self.node,
            tuple(self.challenge),
            self.network,
        ))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES].update({
            'targetUrl': self.target_url,
            'status': self.status.value
        })

        payload[MESSAGE_DATA] = {
            'node': self.node.to_dict(key=True),
            'challenge': self.challenge,
        }

        if self.network is not None:
            payload[MESSAGE_DATA]['network'] = self.network.to_dict()
            payload[MESSAGE_DATA]['network'].pop('nodeIDs', None)
            payload[MESSAGE_DATA]['network'].pop('instanceID')

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> 'AuthRequestInvite':
        network = cls.NETWORK_CLASS.from_dict(payload[MESSAGE_DATA]['network']) if 'network' in payload[
            MESSAGE_DATA] else None
        if network:
            network.node_ids = []

        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageID'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkID'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeID'],
            auth_type=AuthMessageType(payload[MESSAGE_ATTRIBUTES]['authType']),
            status=AuthMessageStatus(payload[MESSAGE_ATTRIBUTES]['status']),
            target_url=payload[MESSAGE_ATTRIBUTES]['targetUrl'],
            node=cls.NODE_CLASS.from_dict(payload[MESSAGE_DATA]['node']),
            challenge=payload[MESSAGE_DATA]['challenge'],
            timestamp=payload['timestamp'],
            network=network,
        )
