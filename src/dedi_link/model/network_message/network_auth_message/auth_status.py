from typing import TypeVar

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import AuthMessageType, AuthMessageStatus
from .network_auth_message import NetworkAuthMessage


AuthStatusType = TypeVar('AuthStatusType', bound='AuthStatus')


class AuthStatus(NetworkAuthMessage):
    def __init__(self,
                 message_id: str,
                 network_id: str,
                 status: AuthMessageStatus | None = None,
                 timestamp: int | None = None,
                 ):
        super().__init__(
            network_id=network_id,
            auth_type=AuthMessageType.STATUS,
            message_id=message_id,
            timestamp=timestamp,
        )

        self.status = status

    def to_dict(self) -> dict:
        payload = super().to_dict()

        if self.status is not None:
            payload[MESSAGE_ATTRIBUTES]['status'] = self.status.value

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> 'AuthStatus':
        status = None

        if 'status' in payload[MESSAGE_ATTRIBUTES]:
            status = AuthMessageStatus(payload[MESSAGE_ATTRIBUTES]['status'])

        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageID'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkID'],
            status=status,
            timestamp=payload['timestamp'],
        )
