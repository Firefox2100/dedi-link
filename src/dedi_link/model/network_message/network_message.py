import uuid
import time
from typing import TypeVar, Type

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType
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
        if not isinstance(other, self.__class__):
            return NotImplemented

        return all([
            self.message_type == other.message_type,
            self.message_id == other.message_id,
            self.timestamp == other.timestamp,
        ])

    def __hash__(self):
        return hash((self.message_type, self.message_id, self.timestamp))

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
        raise BaseModelMethodNotImplemented('NetworkMessage', 'from_dict')

    @classmethod
    def factory(cls: Type[NetworkMessageType], payload: dict) -> NetworkMessageType:
        message_type = MessageType(payload['messageType'])

        from .network_auth_message import NetworkAuthMessage
        from .network_sync_message import NetworkSyncMessage
        from .network_data_message import NetworkDataMessage
        from .network_relay_message import NetworkRelayMessage

        if message_type == MessageType.AUTH_MESSAGE:
            return NetworkAuthMessage.factory(payload)
        if message_type == MessageType.SYNC_MESSAGE:
            return NetworkSyncMessage.factory(payload)
        if message_type == MessageType.DATA_MESSAGE:
            return NetworkDataMessage.factory(payload)
        if message_type == MessageType.RELAY_MESSAGE:
            return NetworkRelayMessage.factory(payload)

        raise ValueError(f'Unknown message type: {payload["messageType"]}')
