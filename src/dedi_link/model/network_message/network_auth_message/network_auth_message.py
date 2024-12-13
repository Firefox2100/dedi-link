import uuid
from enum import Enum
from typing import Type, TypeVar, Callable, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType, AuthMessageType
from ...network import NetworkT
from ...node import NodeT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ..network_message import NetworkMessageB, NetworkMessage
from ..network_message_header import NetworkMessageHeaderT


NetworkAuthMessageBT = TypeVar('NetworkAuthMessageBT', bound='NetworkAuthMessageB')
NetworkAuthMessageT = TypeVar('NetworkAuthMessageT', bound='NetworkAuthMessage')


class NetworkAuthMessageB(NetworkMessageB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                          Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                          ):
    message_type = MessageType.AUTH_MESSAGE
    auth_type: AuthMessageType | None = None

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Base model for a network authorisation message

        This class of messages handle permission, node authorisation, and other
        security-related operations.

        :param network_id: The network ID
        :param node_id: The node ID
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            message_id=message_id or str(uuid.uuid4()),
            network_id=network_id,
            node_id=node_id,
            timestamp=timestamp,
        )

    def __eq__(self, other):
        if not isinstance(other, NetworkAuthMessageB):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.auth_type == other.auth_type,
        ])

    def __hash__(self):
        return hash((super().__hash__(), self.auth_type))

    @classmethod
    def _child_mapping(cls) -> dict[Enum, tuple[Type[NetworkAuthMessageT], Callable[[dict], Enum] | None]]:
        from .auth_request import AuthRequest
        from .auth_invite import AuthInvite
        from .auth_response import AuthResponse
        from .auth_join import AuthJoin
        from .auth_leave import AuthLeave
        from .auth_status import AuthStatus

        return {
            AuthMessageType.REQUEST: (AuthRequest, None),
            AuthMessageType.INVITE: (AuthInvite, None),
            AuthMessageType.RESPONSE: (AuthResponse, None),
            AuthMessageType.JOIN: (AuthJoin, None),
            AuthMessageType.LEAVE: (AuthLeave, None),
            AuthMessageType.STATUS: (AuthStatus, None),
        }

    @classmethod
    def factory(cls: Type[NetworkAuthMessageBT], payload: dict) -> NetworkAuthMessageBT:
        id_var = AuthMessageType(payload[MESSAGE_ATTRIBUTES]['authType'])

        return cls.factory_from_id(
            payload=payload,
            id_var=id_var,
        )

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES]['authType'] = self.auth_type.value

        return payload


class NetworkAuthMessage(NetworkAuthMessageB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                         NetworkMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                         Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                         ):
    pass
