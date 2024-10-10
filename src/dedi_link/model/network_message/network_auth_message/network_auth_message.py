import uuid
from enum import Enum
from typing import Type, TypeVar, Callable

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType, AuthMessageType
from ..network_message import NetworkMessage

NetworkAuthMessageType = TypeVar('NetworkAuthMessageType', bound='NetworkAuthMessage')


class NetworkAuthMessage(NetworkMessage):
    def __init__(self,
                 network_id: str,
                 auth_type: AuthMessageType,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        super().__init__(
            message_type=MessageType.AUTH_MESSAGE,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.network_id = network_id
        self.auth_type = auth_type

    def __eq__(self, other: 'NetworkAuthMessage'):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.network_id == other.network_id,
            self.auth_type == other.auth_type,
        ])

    def __hash__(self):
        return hash((super().__hash__(), self.network_id, self.auth_type))

    @classmethod
    def _child_mapping(cls) -> dict[Enum, tuple[Type[NetworkAuthMessageType], Callable[[dict], Enum] | None]]:
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

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES].update({
            'networkID': self.network_id,
            'authType': self.auth_type.value,
        })

        return payload
