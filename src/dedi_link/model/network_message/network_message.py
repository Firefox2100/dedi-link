import uuid
import time
from enum import Enum
from typing import TypeVar, Type, Callable

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType, AuthMessageType
from dedi_link.etc.exceptions import NetworkMessageNotImplementedException
from ..base_model import BaseModel


NetworkMessageType = TypeVar('NetworkMessageType', bound='NetworkMessage')


class NetworkMessage(BaseModel):
    def __init__(self,
                 message_type: MessageType,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        self.message_type = message_type
        self.message_id = message_id or str(uuid.uuid4())
        self.timestamp = timestamp or int(time.time())

    def __eq__(self, other: 'NetworkMessage'):
        if not isinstance(other, NetworkMessage):
            return NotImplemented

        return all([
            self.message_type == other.message_type,
            self.message_id == other.message_id,
            self.timestamp == other.timestamp,
        ])

    def __hash__(self):
        return hash((self.message_type, self.message_id, self.timestamp))

    @classmethod
    def _child_mapping(cls) -> dict[Enum, tuple[Type[NetworkMessageType], Callable[[dict], Enum] | None]]:
        from .network_auth_message import NetworkAuthMessage
        from .network_sync_message import NetworkSyncMessage
        from .network_data_message import NetworkDataMessage
        from .network_relay_message import NetworkRelayMessage

        return {
            MessageType.AUTH_MESSAGE: (NetworkAuthMessage, lambda payload: AuthMessageType(payload['messageAttribute']['authType'])),
            MessageType.SYNC_MESSAGE: (NetworkSyncMessage, None),
            MessageType.DATA_MESSAGE: (NetworkDataMessage, ),
            MessageType.RELAY_MESSAGE: (NetworkRelayMessage, None),
        }

    def to_dict(self) -> dict:
        payload = {
            'messageType': self.message_type.value,
            MESSAGE_ATTRIBUTES: {
                'messageID': self.message_id,
            },
            'timestamp': self.timestamp,
        }

        return payload

    @classmethod
    def from_dict(cls: Type[NetworkMessageType], payload: dict) -> NetworkMessageType:
        raise NetworkMessageNotImplementedException('from_dict method not implemented')
