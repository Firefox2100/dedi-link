from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES, MESSAGE_DATA
from dedi_link.etc.enums import AuthMessageType
from ...node import Node, NodeType
from ...network import Network, NetworkType
from .network_auth_message import NetworkAuthMessage


AuthResponseType = TypeVar('AuthResponseType', bound='AuthResponse')


class AuthResponse(NetworkAuthMessage, Generic[NodeType, NetworkType]):
    """
    Network Authorization Response Message

    This message is used to respond to a previous request or invitation.
    It should carry information the counterparty does not know. For example,
    if the previous message is a request, then the response should carry the
    network information.
    """
    NODE_CLASS = Node
    NETWORK_CLASS = Network

    def __init__(self,
                 message_id: str,
                 approved: bool,
                 node: NodeType | None = None,
                 timestamp: int | None = None,
                 network: NetworkType | None = None,
                 ):
        super().__init__(
            network_id='',
            auth_type=AuthMessageType.RESPONSE,
            message_id=message_id,
            timestamp=timestamp,
        )

        self.approved = approved
        self.node = node
        self.network = network

        if self.approved:
            if self.node is None:
                raise ValueError('Approved response must have a Node object to represent this node')

            self.network_id = self.network.network_id

    def __eq__(self, other: 'AuthResponse'):
        if not isinstance(other, AuthResponse):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.approved == other.approved,
            self.node == other.node,
            self.network == other.network,
        ])

    def __hash__(self):
        return hash((super().__hash__(), self.approved, self.node, self.network))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES]['approved'] = self.approved

        message_data = {}

        if self.node is not None:
            message_data['node'] = self.node.to_dict(key=True)

        if self.network is not None:
            message_data['network'] = self.network.to_dict()
            message_data['network'].pop('nodeIDs', None)
            message_data['network'].pop('instanceID')

        if message_data:
            payload[MESSAGE_DATA] = message_data

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> 'AuthResponse':
        node = None
        network = None

        if MESSAGE_DATA in payload:
            if 'node' in payload[MESSAGE_DATA]:
                node = cls.NODE_CLASS.from_dict(payload[MESSAGE_DATA]['node'])

            if 'network' in payload[MESSAGE_DATA]:
                network = cls.NETWORK_CLASS.from_dict(payload[MESSAGE_DATA]['network'])

        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageID'],
            approved=payload[MESSAGE_ATTRIBUTES]['approved'],
            node=node,
            timestamp=payload['timestamp'],
            network=network,
        )
