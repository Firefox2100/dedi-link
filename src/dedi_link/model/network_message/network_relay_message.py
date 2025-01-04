"""
Network Relay Message
"""

from copy import deepcopy
from collections import Counter
from typing import TypeVar, Generic, Type
from deepdiff import DeepDiff

from dedi_link.etc.consts import MESSAGE_DATA, MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType
from dedi_link.etc.exceptions import NetworkRelayMessageEnvelopeTooDeep, NetworkRelayMessageNotAlive, \
    NetworkMessageNotImplemented
from ..base_model import BaseModel
from ..network import NetworkT
from ..node import NodeT
from ..data_index import DataIndexT
from ..user_mapping import UserMappingT
from .network_message import NetworkMessageBase, NetworkMessage, NetworkMessageT
from .network_message_header import NetworkMessageHeader, NetworkMessageHeaderT


RelayTargetT = TypeVar('RelayTargetT', bound='RelayTarget')
NetworkRelayMessageBaseT = TypeVar('NetworkRelayMessageBaseT', bound='NetworkRelayMessageBase')
NetworkRelayMessageT = TypeVar('NetworkRelayMessageT', bound='NetworkRelayMessage')


class RelayTarget(BaseModel,
                  Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                  ):
    """
    Relay Target

    A data structure to hold the recipient ID, header, and message of
    a message being relayed.
    """
    NETWORK_MESSAGE_HEADER_CLASS = NetworkMessageHeader
    NETWORK_MESSAGE_CLASS = NetworkMessage[
        NetworkMessageHeaderT,
        NetworkT,
        DataIndexT,
        UserMappingT,
        NodeT
    ]

    def __init__(self,
                 recipient_ids: list[str],
                 route: list[str],
                 header: NetworkMessageHeaderT,
                 message: NetworkMessageT,
                 ):
        """
        Relay Target

        A data structure to hold the recipient ID, header, and message of
        a message being relayed.

        :param recipient_ids: The recipient IDs
        :param route: A list of node IDs from the sender to the last relay,
        storing route information
        :param header: The header of the message
        :param message: The message being relayed
        """
        self.recipient_ids = recipient_ids
        self.route = route
        self.header = header
        self.message = message

        if message.message_type == MessageType.RELAY_MESSAGE:
            raise NetworkRelayMessageEnvelopeTooDeep(
                'Relay message cannot be sent in another relay message'
            )

        if self.header.node_id != self.message.node_id:
            raise ValueError('Header node ID does not match message node ID')

        if not self.route:
            self.route.extend([self.header.node_id])
        elif self.route[0] != self.header.node_id:
            raise ValueError('Route does not start with header node ID')

    def __eq__(self, other):
        if not isinstance(other, RelayTarget):
            return NotImplemented

        return all([
            not DeepDiff(self.recipient_ids, other.recipient_ids, ignore_order=True),
            self.route == other.route,
            self.header == other.header,
            self.message == other.message,
        ])

    def __hash__(self):
        recipient_ids = deepcopy(self.recipient_ids)
        recipient_ids.sort()

        return hash((
            tuple(recipient_ids),
            tuple(self.route),
            self.header,
            self.message,
        ))

    def to_dict(self) -> dict:
        return {
            'recipientIds': self.recipient_ids,
            'route': self.route,
            'header': self.header.headers,
            'message': self.message.to_dict(),
        }

    @classmethod
    def from_dict(cls: Type[RelayTargetT], payload: dict) -> RelayTargetT:
        return cls(
            recipient_ids=payload['recipientIds'],
            route=payload['route'],
            header=cls.NETWORK_MESSAGE_HEADER_CLASS.from_headers(payload['header']),
            message=cls.NETWORK_MESSAGE_CLASS.factory(payload['message']),
        )


class NetworkRelayMessageBase(NetworkMessageBase[
                                  NetworkMessageHeaderT,
                                  NetworkT,
                                  DataIndexT,
                                  UserMappingT,
                                  NodeT,
                              ],
                              Generic[
                                  NetworkMessageHeaderT,
                                  NetworkT,
                                  DataIndexT,
                                  UserMappingT,
                                  NodeT
                              ]):
    """
    Base class for Network Relay Messages
    """
    RELAY_TARGET_CLASS = RelayTarget
    message_type = MessageType.RELAY_MESSAGE

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 relay_targets: list[RelayTarget],
                 ttl: int = 3,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Network Relay Message

        These messages are used to relay messages between nodes in a network.

        :param network_id: The network ID
        :param node_id: The node ID
        :param relay_targets: A list of RelayTarget instances
        :param ttl: The time-to-live of the relay message, in hops.
                    Direct delivery counts as one hop.
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            message_id=message_id,
            timestamp=timestamp,
        )

        self.relay_targets = relay_targets
        self.ttl = ttl

        if ttl <= 0:
            raise NetworkRelayMessageNotAlive('Relay message TTL must be greater than 0')

    def __eq__(self, other: NetworkRelayMessageBaseT):
        if not isinstance(other, NetworkRelayMessageBase):
            return NotImplemented

        return all([
            super().__eq__(other),
            Counter(self.relay_targets) == Counter(other.relay_targets),
            self.ttl == other.ttl,
        ])

    def __hash__(self):
        # Sort the relay targets by recipient ID to ensure the hash is consistent
        relay_targets = deepcopy(self.relay_targets)
        for target in relay_targets:
            target.recipient_ids.sort()

        relay_targets.sort(key=lambda x: x.recipient_ids)

        return hash((
            super().__hash__(),
            tuple(relay_targets),
            self.ttl,
        ))

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload[MESSAGE_ATTRIBUTES].update({
            'ttl': self.ttl,
        })

        payload[MESSAGE_DATA] = {
            'relayTargets': [target.to_dict() for target in self.relay_targets],
        }

        return payload

    @classmethod
    def from_dict(cls: Type[NetworkRelayMessageBaseT], payload: dict) -> NetworkRelayMessageBaseT:
        return cls(
            message_id=payload[MESSAGE_ATTRIBUTES]['messageId'],
            network_id=payload[MESSAGE_ATTRIBUTES]['networkId'],
            node_id=payload[MESSAGE_ATTRIBUTES]['nodeId'],
            timestamp=payload['timestamp'],
            ttl=payload[MESSAGE_ATTRIBUTES]['ttl'],
            relay_targets=[
                cls.RELAY_TARGET_CLASS.from_dict(target)
                    for target in payload[MESSAGE_DATA]['relayTargets']
            ],
        )


class NetworkRelayMessage(NetworkRelayMessageBase[
                              NetworkMessageHeaderT,
                              NetworkT,
                              DataIndexT,
                              UserMappingT,
                              NodeT
                          ],
                          NetworkMessage[
                              NetworkMessageHeaderT,
                              NetworkT,
                              DataIndexT,
                              UserMappingT,
                              NodeT
                          ],
                          Generic[
                              NetworkMessageHeaderT,
                              NetworkT,
                              DataIndexT,
                              UserMappingT,
                              NodeT
                          ]):
    """
    Network Relay Message

    These messages are used to relay messages between nodes in a network.
    """
    @classmethod
    def load_polling(cls: Type[NetworkRelayMessageT]) -> list[NetworkRelayMessageT]:
        """
        Load all polling messages from the storage

        :return: A list of polling messages
        """
        raise NetworkMessageNotImplemented(
            'load_polling method must be implemented in library implementation'
        )
