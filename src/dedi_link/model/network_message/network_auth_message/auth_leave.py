import uuid
from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import AuthMessageType
from ...network import NetworkT
from ..network_message_header import NetworkMessageHeaderT
from .network_auth_message import NetworkAuthMessageB, NetworkAuthMessage


AuthLeaveBT = TypeVar('AuthLeaveBT', bound='AuthLeaveB')
AuthLeaveT = TypeVar('AuthLeaveT', bound='AuthLeave')


class AuthLeaveB(NetworkAuthMessageB[NetworkMessageHeaderT, NetworkT],
                Generic[NetworkMessageHeaderT, NetworkT]
                ):
    def __init__(self,
                 node_id: str,
                 network_id: str,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Base class for Network Authorization Leave Message

        :param network_id: The network ID
        :param node_id: The node ID
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            auth_type=AuthMessageType.LEAVE,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

    @classmethod
    def from_dict(cls, payload: dict) -> AuthLeaveBT:
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            timestamp=payload['timestamp'],
        )


class AuthLeave(AuthLeaveB[NetworkMessageHeaderT, NetworkT],
                NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                Generic[NetworkMessageHeaderT, NetworkT]
                ):
    """
    Network Authorization Leave Message

    This message notifies the other nodes within the network about
    this node leaving. The others are expected to remove all information
    about this node.
    """
