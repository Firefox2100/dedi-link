"""
Network Authorisation Leave Message
"""

from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import AuthMessageType
from ...network import NetworkT
from ...node import NodeT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ..network_message_header import NetworkMessageHeaderT
from .network_auth_message import NetworkAuthMessageBase, NetworkAuthMessage


AuthLeaveBaseT = TypeVar('AuthLeaveBaseT', bound='AuthLeaveBase')
AuthLeaveT = TypeVar('AuthLeaveT', bound='AuthLeave')


class AuthLeaveBase(NetworkAuthMessageBase[
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
    The base model for Auth Leave Messages
    """

    auth_type = AuthMessageType.LEAVE

    def __init__(self,
                 node_id: str,
                 network_id: str,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Base class for Network Authorisation Leave Message

        :param network_id: The network ID
        :param node_id: The node ID
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            message_id=message_id,
            timestamp=timestamp,
        )

    @classmethod
    def from_dict(cls, payload: dict) -> AuthLeaveBaseT:
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            timestamp=payload['timestamp'],
        )


class AuthLeave(AuthLeaveBase[
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
                ]
                ):
    """
    Network Authorisation Leave Message

    This message notifies the other nodes within the network about
    this node leaving. The others are expected to remove all information
    about this node.
    """
