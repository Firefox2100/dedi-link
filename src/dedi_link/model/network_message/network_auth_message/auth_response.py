from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES, MESSAGE_DATA
from dedi_link.etc.enums import AuthMessageType
from ...node import Node, NodeType
from ...network import Network, NetworkType
from .network_auth_message import NetworkAuthMessage


AuthResponseType = TypeVar('AuthResponseType', bound='AuthResponse')


class AuthResponse(NetworkAuthMessage, Generic[NodeType, NetworkType]):
    NODE_CLASS = Node
    NETWORK_CLASS = Network

    def __init__(self,
                 message_id: str,
                 approved: bool,
                 network_id: str = '',
                 node_id: str = '',
                 node: NodeType | None = None,
                 timestamp: int | None = None,
                 network: NetworkType | None = None,
                 ):
        """
        Network Authorisation Response Message

        This message is used to respond to a previous request or invitation.
        It should carry information the counterparty does not know. For example,
        if the previous message is a request, then the response should carry the
        network information.

        :param message_id: The message ID
        :param approved: Whether the request is approved
        :param network_id: The network ID
        :param node_id: The node ID
        :param node: The node that is responding; only present if approved
        :param timestamp: The timestamp in seconds since epoch
        :param network: The network information; only present if approved, and the
                        previous message is a request
        """
        super().__init__(
            network_id=network_id,
            node_id=node_id,
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

            if self.node_id != self.node.node_id:
                raise ValueError('Node ID must match the Node object')

            if self.network is not None:
                if self.network.network_id != self.network_id:
                    raise ValueError('Network ID must match the Network object')

    def __eq__(self, other: 'AuthResponse'):
        if not isinstance(other, AuthResponse):
            return NotImplemented

        self_network = self.network
        other_network = other.network

        if self.network is not None and other.network is not None:
            self_network.node_ids = []
            other_network.node_ids = []

        return all([
            super().__eq__(other),
            self.approved == other.approved,
            self.node == other.node,
            self_network == other_network,
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
            message_data['network'].pop('nodeIds', None)
            message_data['network'].pop('instanceId')

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
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            approved=payload[MESSAGE_ATTRIBUTES]['approved'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            node=node,
            timestamp=payload['timestamp'],
            network=network,
        )
