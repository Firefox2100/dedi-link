import uuid
from enum import Enum
from typing import Type, TypeVar, Callable, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType, AuthMessageType
from ...network import NetworkT
from ..network_message import NetworkMessageB, NetworkMessage
from ..network_message_header import NetworkMessageHeaderT



NetworkAuthMessageT = TypeVar('NetworkAuthMessageT', bound='NetworkAuthMessage')


class NetworkAuthMessageB(NetworkMessageB[NetworkMessageHeaderT, NetworkT],
                          Generic[NetworkMessageHeaderT, NetworkT]
                          ):
    def __init__(self,
                 network_id: str,
                 node_id: str,
                 auth_type: AuthMessageType,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Base model for a network authorisation message

        This class of messages handle permission, node authorisation, and other
        security-related operations.

        :param network_id: The network ID
        :param node_id: The node ID
        :param auth_type: The type of authorisation message
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            message_type=MessageType.AUTH_MESSAGE,
            message_id=message_id or str(uuid.uuid4()),
            network_id=network_id,
            node_id=node_id,
            timestamp=timestamp,
        )

        self.auth_type = auth_type

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
        from .auth_request_invite import AuthRequestInvite
        from .auth_response import AuthResponse
        from .auth_join import AuthJoin
        from .auth_leave import AuthLeave
        from .auth_status import AuthStatus

        return {
            AuthMessageType.REQUEST: (AuthRequestInvite, None),
            AuthMessageType.INVITE: (AuthRequestInvite, None),
            AuthMessageType.RESPONSE: (AuthResponse, None),
            AuthMessageType.JOIN: (AuthJoin, None),
            AuthMessageType.LEAVE: (AuthLeave, None),
            AuthMessageType.STATUS: (AuthStatus, None),
        }

    @classmethod
    def factory(cls, payload: dict):
        id_var = AuthMessageType(payload[MESSAGE_ATTRIBUTES]['authType'])

        return cls.factory_from_id(
            payload=payload,
            id_var=id_var,
        )

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES]['authType'] = self.auth_type.value

        return payload


class NetworkAuthMessage(NetworkAuthMessageB[NetworkMessageHeaderT, NetworkT],
                         NetworkMessage[NetworkMessageHeaderT, NetworkT],
                         Generic[NetworkMessageHeaderT, NetworkT]
                         ):
    pass
