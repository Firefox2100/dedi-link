from copy import deepcopy
from deepdiff import DeepDiff
from typing import TypeVar, Generic

from dedi_link.etc.consts import MESSAGE_DATA, MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType
from dedi_link.etc.exceptions import NetworkRelayMessageEnvelopeTooDeep, NetworkRelayMessageNotAlive
from ..base_model import BaseModel
from ..network import NetworkT
from .network_message import NetworkMessageB, NetworkMessage, NetworkMessageT
from .network_message_header import NetworkMessageHeader, NetworkMessageHeaderT


RelayTargetT = TypeVar('RelayTargetT', bound='RelayTarget')
NetworkRelayMessageBT = TypeVar('NetworkRelayMessageBT', bound='NetworkRelayMessageB')
NetworkRelayMessageT = TypeVar('NetworkRelayMessageT', bound='NetworkRelayMessage')


class RelayTarget(BaseModel,
                  Generic[NetworkMessageHeaderT, NetworkMessageT]
                  ):
    """
    Relay Target

    A data structure to hold the recipient ID, header, and message of
    a message being relayed.
    """
    NETWORK_MESSAGE_HEADER_CLASS = NetworkMessageHeader
    NETWORK_MESSAGE_CLASS = NetworkMessage

    def __init__(self,
                 recipient_ids: list[str],
                 header: NetworkMessageHeaderT,
                 message: NetworkMessageT,
                 ):
        """
        Relay Target

        A data structure to hold the recipient ID, header, and message of
        a message being relayed.

        :param recipient_ids: The recipient IDs
        :param header: The header of the message
        :param message: The message being relayed
        """
        self.recipient_ids = recipient_ids
        self.header = header
        self.message = message

        if message.message_type == MessageType.RELAY_MESSAGE:
            raise NetworkRelayMessageEnvelopeTooDeep('Relay message cannot be sent in another relay message')

    def to_dict(self) -> dict:
        return {
            'recipientIds': self.recipient_ids,
            'header': self.header.headers,
            'message': self.message.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: dict) -> RelayTargetT:
        return cls(
            recipient_ids=payload['recipientIds'],
            header=cls.NETWORK_MESSAGE_HEADER_CLASS.from_headers(payload['header']),
            message=cls.NETWORK_MESSAGE_CLASS.factory(payload['message']),
        )


class NetworkRelayMessageB(NetworkMessageB[NetworkMessageHeaderT, NetworkT],
                           Generic[NetworkMessageHeaderT, NetworkT, RelayTargetT]
                           ):
    """
    Base class for Network Relay Messages
    """
    RELAY_TARGET_CLASS = RelayTarget

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 sender_id: str,
                 relay_targets: list[RelayTargetT],
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
        :param relay_targets: A list of RelayTarget instances
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
        self.relay_targets = relay_targets
        self.ttl = ttl

        if ttl <= 0:
            raise NetworkRelayMessageNotAlive('Relay message TTL must be greater than 0')

    def __eq__(self, other: NetworkRelayMessageBT):
        if not isinstance(other, NetworkRelayMessageB):
            return NotImplemented

        return all([
            super().__eq__(other),
            self.sender_id == other.sender_id,
            not DeepDiff(self.relay_targets, other.relay_targets, ignore_order=True),
            self.ttl == other.ttl,
        ])

    def __hash__(self):
        # Sort the relay targets by recipient ID to ensure the hash is consistent
        relay_targets = deepcopy(self.relay_targets)
        relay_targets.sort(key=lambda x: x.recipient_id)

        return hash((
            super().__hash__(),
            self.sender_id,
            tuple(relay_targets),
            self.ttl,
        ))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES].update({
            'senderId': self.sender_id,
            'ttl': self.ttl,
        })

        payload[MESSAGE_DATA] = {
            'relayTargets': [target.to_dict() for target in self.relay_targets],
        }

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> NetworkRelayMessageBT:
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            sender_id=payload[MESSAGE_ATTRIBUTES]['senderId'],
            timestamp=payload['timestamp'],
            ttl=payload[MESSAGE_ATTRIBUTES]['ttl'],
            relay_targets=[
                cls.RELAY_TARGET_CLASS.from_dict(target) for target in payload[MESSAGE_DATA]['relayTargets']
            ],
        )


class NetworkRelayMessage(NetworkRelayMessageB[NetworkMessageHeaderT, NetworkT, RelayTargetT],
                          NetworkMessage[NetworkMessageHeaderT, NetworkT],
                          Generic[NetworkMessageHeaderT, NetworkT, RelayTargetT],
                          ):
    """
    Network Relay Message

    These messages are used to relay messages between nodes in a network.
    """
