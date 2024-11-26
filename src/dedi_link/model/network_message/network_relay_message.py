import uuid
from copy import deepcopy
from typing import TypeVar

from dedi_link.etc.consts import MESSAGE_DATA, MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType
from dedi_link.etc.exceptions import NetworkRelayMessageEnvelopeTooDeep, NetworkRelayMessageNotAlive
from .network_message import NetworkMessage
from .network_message_header import NetworkMessageHeader


NetworkRelayMessageT = TypeVar('NetworkRelayMessageT', bound='NetworkRelayMessage')


class NetworkRelayMessage(NetworkMessage):
    """
    Network Relay Message

    These messages are used to relay messages between nodes in a network.
    """
    def __init__(self,
                 sender_id: str,
                 recipient_ids: list[str],
                 headers: NetworkMessageHeader,
                 message: NetworkMessage,
                 ttl: int = 3,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        super().__init__(
            message_type=MessageType.RELAY_MESSAGE,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.sender_id = sender_id
        self.recipient_ids = recipient_ids
        self.headers = headers
        self.message = message
        self.ttl = ttl

        if message.message_type == MessageType.RELAY_MESSAGE:
            raise NetworkRelayMessageEnvelopeTooDeep('Relay message cannot be sent in another relay message')

        if ttl <= 0:
            raise NetworkRelayMessageNotAlive('Relay message TTL must be greater than 0')

    def __eq__(self, other: 'NetworkRelayMessage'):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.sender_id == other.sender_id,
            self.recipient_ids == other.recipient_ids,
            self.headers == other.headers,
            self.message == other.message,
            self.ttl == other.ttl,
        ])

    def __hash__(self):
        recipient_ids = deepcopy(self.recipient_ids)
        recipient_ids.sort()

        return hash((
            super().__hash__(),
            self.sender_id,
            tuple(recipient_ids),
            self.headers,
            self.message,
            self.ttl,
        ))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES].update({
            'senderID': self.sender_id,
            'recipientIDs': self.recipient_ids,
            'ttl': self.ttl,
        })

        payload[MESSAGE_DATA] = {
            'headers': self.headers.headers,
            'message': self.message.to_dict(),
        }

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> 'NetworkRelayMessage':
        enveloped_message_type = MessageType(payload[MESSAGE_DATA]['message']['messageType'])

        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageID'],
            sender_id=payload[MESSAGE_ATTRIBUTES]['senderID'],
            recipient_ids=payload[MESSAGE_ATTRIBUTES]['recipientIDs'],
            timestamp=payload['timestamp'],
            ttl=payload[MESSAGE_ATTRIBUTES]['ttl'],
            headers=NetworkMessageHeader.from_headers(payload[MESSAGE_DATA]['headers']),
            message=NetworkMessage.factory(payload[MESSAGE_DATA]['message'], enveloped_message_type),
        )
