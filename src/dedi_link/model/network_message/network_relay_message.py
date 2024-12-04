from copy import deepcopy
from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_DATA, MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType
from dedi_link.etc.exceptions import NetworkRelayMessageEnvelopeTooDeep, NetworkRelayMessageNotAlive
from ..network import NetworkT
from .network_message import NetworkMessageB, NetworkMessage
from .network_message_header import NetworkMessageHeader, NetworkMessageHeaderT


NetworkRelayMessageBT = TypeVar('NetworkRelayMessageBT', bound='NetworkRelayMessageB')
NetworkRelayMessageT = TypeVar('NetworkRelayMessageT', bound='NetworkRelayMessage')


class NetworkRelayMessageB(NetworkMessageB[NetworkMessageHeaderT, NetworkT],
                           Generic[NetworkMessageHeaderT, NetworkT]
                           ):
    """
    Base class for Network Relay Messages
    """
    def __init__(self,
                 network_id: str,
                 node_id: str,
                 sender_id: str,
                 recipient_ids: list[str],
                 headers: NetworkMessageHeader,
                 message: NetworkMessage,
                 ttl: int = 3,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Network Relay Message

        These messages are used to relay messages between nodes in a network.

        :param network_id: The network ID
        :param node_id: The node ID
        :param sender_id: The sender ID
        :param recipient_ids: The recipient IDs
        :param headers: The message headers
        :param message: The message to relay
        :param ttl: The time-to-live of the relay message, in hops.
                    Direct delivery counts as one hop.
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            message_type=MessageType.RELAY_MESSAGE,
            network_id=network_id,
            node_id=node_id,
            message_id=message_id,
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

    def __eq__(self, other: NetworkRelayMessageBT):
        if not isinstance(other, NetworkRelayMessageB):
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
            'senderId': self.sender_id,
            'recipientIds': self.recipient_ids,
            'ttl': self.ttl,
        })

        payload[MESSAGE_DATA] = {
            'headers': self.headers.headers,
            'message': self.message.to_dict(),
        }

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> NetworkRelayMessageBT:
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            sender_id=payload[MESSAGE_ATTRIBUTES]['senderId'],
            recipient_ids=payload[MESSAGE_ATTRIBUTES]['recipientIds'],
            timestamp=payload['timestamp'],
            ttl=payload[MESSAGE_ATTRIBUTES]['ttl'],
            headers=NetworkMessageHeader.from_headers(payload[MESSAGE_DATA]['headers']),
            message=NetworkMessage.factory(payload[MESSAGE_DATA]['message']),
        )


class NetworkRelayMessage(NetworkRelayMessageB[NetworkMessageHeaderT, NetworkT],
                          NetworkMessage[NetworkMessageHeaderT, NetworkT],
                          Generic[NetworkMessageHeaderT, NetworkT],
                          ):
    """
    Network Relay Message

    These messages are used to relay messages between nodes in a network.
    """
