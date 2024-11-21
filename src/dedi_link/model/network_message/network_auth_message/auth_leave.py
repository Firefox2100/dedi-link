import uuid
from typing import TypeVar

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import AuthMessageType
from .network_auth_message import NetworkAuthMessage


AuthLeaveType = TypeVar('AuthLeaveType', bound='AuthLeave')


class AuthLeave(NetworkAuthMessage):
    def __init__(self,
                 node_id: str,
                 network_id: str,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            auth_type=AuthMessageType.LEAVE,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

    @classmethod
    def from_dict(cls, payload: dict) -> 'AuthLeave':
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            timestamp=payload['timestamp'],
        )
