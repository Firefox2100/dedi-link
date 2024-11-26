from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import AuthMessageType, AuthMessageStatus
from ...network import NetworkT
from ..network_message_header import NetworkMessageHeaderT
from .network_auth_message import NetworkAuthMessage


AuthStatusT = TypeVar('AuthStatusT', bound='AuthStatus')


class AuthStatus(NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                 Generic[NetworkMessageHeaderT, NetworkT]
                 ):
    def __init__(self,
                 message_id: str,
                 network_id: str,
                 node_id: str,
                 status: AuthMessageStatus | None = None,
                 timestamp: int | None = None,
                 ):
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            auth_type=AuthMessageType.STATUS,
            message_id=message_id,
            timestamp=timestamp,
        )

        self.status = status

    def __eq__(self, other):
        if not isinstance(other, AuthStatus):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.status == other.status
        ])

    def __hash__(self):
        return hash((
            super().__hash__(),
            self.status
        ))

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
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            status=status,
            timestamp=payload['timestamp'],
        )
