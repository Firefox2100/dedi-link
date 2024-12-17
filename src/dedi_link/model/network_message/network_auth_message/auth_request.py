"""
Network Authorization Request Message
"""

import uuid
import secrets
from typing import TypeVar, Generic, Type
from deepdiff import DeepDiff

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES, MESSAGE_DATA
from dedi_link.etc.enums import AuthMessageType, AuthMessageStatus
from ...node import Node, NodeT
from ...network import NetworkT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ...config import DdlConfig
from ..network_message_header import NetworkMessageHeaderT
from .network_auth_message import NetworkAuthMessageBase, NetworkAuthMessage


AuthRequestBaseT = TypeVar('AuthRequestBaseT', bound='AuthRequestBase')
AuthRequestT = TypeVar('AuthRequestT', bound='AuthRequest')


class AuthRequestBase(NetworkAuthMessageBase[
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
    Base model for Network Authorization Request or Invite Message
    """

    NODE_CLASS = Node[DataIndexT, UserMappingT]
    auth_type = AuthMessageType.REQUEST

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 status: AuthMessageStatus,
                 node: Node,
                 target_url: str,
                 challenge: list[str] = None,
                 justification: str = '',
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Network Authorization Request Message

        This message is for requesting to join a network by asking a "seeder" node.

        :param network_id: The network ID
        :param node_id: The node ID
        :param status: The status of the request
        :param node: The node that is joining or being invited
        :param target_url: The URL to send the response to
        :param challenge: The security challenge
        :param justification: The reason for the request
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.status = status
        self.target_url = target_url
        self.node = node
        self.challenge = challenge
        self.justification = justification

        if self.challenge is None:
            self.generate_challenge()

        if self.node_id != self.node.node_id:
            raise ValueError('Node ID mismatch')

    def __eq__(self, other):
        if not isinstance(other, AuthRequestBase):
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
        ])

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.status,
            self.target_url,
            self.node,
            tuple(self.challenge),
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

        if self.justification:
            payload[MESSAGE_DATA]['justification'] = self.justification

        return payload

    @classmethod
    def from_dict(cls: Type[AuthRequestBaseT], payload: dict) -> AuthRequestBaseT:
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            status=AuthMessageStatus(payload[MESSAGE_ATTRIBUTES]['status']),
            target_url=payload[MESSAGE_ATTRIBUTES]['targetUrl'],
            node=cls.NODE_CLASS.from_dict(payload[MESSAGE_DATA]['node']),
            challenge=payload[MESSAGE_DATA]['challenge'],
            justification=payload[MESSAGE_DATA].get('justification', ''),
            timestamp=payload['timestamp'],
        )

    def generate_challenge(self) -> list[str]:
        """
        Generate three random words for security verification

        The words are taken from BIP-0039 word list, but the generation process
        is not tied to the request itself like most BIP-0039 implementations.
        The words cannot be reproduced from the request, or used to recover the
        request information.

        :return: A list of three random words
        """
        challenge = []

        words = DdlConfig().bip_39

        while len(challenge) < 3:
            word = secrets.choice(words).strip()
            if word not in challenge:
                challenge.append(word)

        self.challenge = challenge

        return challenge


class AuthRequest(AuthRequestBase[
                      NetworkMessageHeaderT,
                      NetworkT,
                      DataIndexT,
                      UserMappingT,
                      NodeT
                  ],
                  NetworkAuthMessage[
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
    Network Authorisation Request Message

    This message is for requesting to join a network by asking a node,
    or to invite a node to join a network that this node is in.
    """
    def update_status(self, status: AuthMessageStatus):
        """
        Wrapper method to update the status of the request

        :param status: The new status
        """
        self.status = status

        self.update({
            'status': status.value,
        })
