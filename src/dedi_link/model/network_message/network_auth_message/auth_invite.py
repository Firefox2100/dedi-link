"""
Network Authorisation Invite Message
"""

from typing import TypeVar, Generic, Type
from copy import deepcopy

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES, MESSAGE_DATA
from dedi_link.etc.enums import AuthMessageType, AuthMessageStatus
from ...node import Node, NodeT
from ...network import Network, NetworkT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ..network_message_header import NetworkMessageHeaderT
from .auth_request import AuthRequestBase, AuthRequest


AuthInviteBaseT = TypeVar('AuthInviteBaseT', bound='AuthInviteBase')
AuthInviteT = TypeVar('AuthInviteT', bound='AuthInvite')


class AuthInviteBase(AuthRequestBase[
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
    Base model for Network Authorization Invite Message
    """

    auth_type = AuthMessageType.INVITE

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 status: AuthMessageStatus,
                 node: Node,
                 network: Network,
                 target_url: str,
                 challenge: list[str] = None,
                 justification: str = '',
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Network Authorization Invite Message

        This message is for requesting another node to join a
        network this node is already a part of.

        :param network_id: The network ID
        :param node_id: The node ID
        :param status: The status of the request
        :param node: The node that is joining or being invited
        :param network: The network for the request
        :param target_url: The URL to send the response to
        :param challenge: The security challenge
        :param justification: The reason for the request
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            status=status,
            node=node,
            target_url=target_url,
            challenge=challenge,
            justification=justification,
            message_id=message_id,
            timestamp=timestamp,
        )

        self.network = network

        if self.network_id != self.network.network_id:
            raise ValueError('Network ID mismatch')

        if self.node_id != self.network.instance_id:
            raise ValueError('Node ID must match the instance ID of the network')

    def __eq__(self, other):
        if not isinstance(other, AuthInviteBase):
            return NotImplemented

        self_network = deepcopy(self.network)
        other_network = deepcopy(other.network)

        if self_network is not None and other_network is not None:
            # Remove the instance ID and node IDs from the network object
            # They are expected to be different
            self_network.instance_id = None
            self_network.node_ids = []
            other_network.instance_id = None
            other_network.node_ids = []

        return all([
            super().__eq__(other),
            self_network == other_network,
        ])

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.network,
        ))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_DATA]['network'] = self.network.to_dict()
        payload[MESSAGE_DATA]['network'].pop('nodeIds', None)
        payload[MESSAGE_DATA]['network'].pop('instanceId')

        return payload

    @classmethod
    def from_dict(cls: Type[AuthInviteBaseT], payload: dict) -> AuthInviteBaseT:
        network = cls.NETWORK_CLASS.from_dict(
            payload[MESSAGE_DATA]['network']
        )
        network.node_ids = []

        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            status=AuthMessageStatus(payload[MESSAGE_ATTRIBUTES]['status']),
            target_url=payload[MESSAGE_ATTRIBUTES]['targetUrl'],
            node=cls.NODE_CLASS.from_dict(payload[MESSAGE_DATA]['node']),
            network=network,
            challenge=payload[MESSAGE_DATA]['challenge'],
            justification=payload[MESSAGE_DATA].get('justification', ''),
            timestamp=payload['timestamp'],
        )


class AuthInvite(AuthInviteBase[
                     NetworkMessageHeaderT,
                     NetworkT,
                     DataIndexT,
                     UserMappingT,
                     NodeT
                 ],
                 AuthRequest[
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
    Network Authorization Invite Message

    This message is for requesting another node to join a
    network this node is already a part of.
    """
