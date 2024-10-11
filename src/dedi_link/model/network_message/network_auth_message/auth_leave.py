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
            auth_type=AuthMessageType.LEAVE,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.node_id = node_id

    def __eq__(self, other: 'AuthLeave'):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.node_id == other.node_id,
        ])

    def __hash__(self):
        return hash((super().__hash__(), self.node_id))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES]['nodeID'] = self.node_id

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> AuthLeaveType:
        message_id = payload[MESSAGE_ATTRIBUTES]['messageID']
        network_id = payload[MESSAGE_ATTRIBUTES]['networkID']
        node_id = payload[MESSAGE_ATTRIBUTES]['nodeID']
        timestamp = payload['timestamp']

        return cls(
            message_id=message_id,
            network_id=network_id,
            node_id=node_id,
            timestamp=timestamp,
        )
