"""
Enum values for the decentralised discovery link

In this library, all enums are serialised into their string values when
converted to JSON or dict.
"""

from enum import Enum


class MappingType(Enum):
    """
    User mapping types
    """
    NO_MAPPING = 'noMapping'
    STATIC = 'static'
    DYNAMIC = 'dynamic'


class MessageType(Enum):
    """
    Types of messages passed in the network protocol
    """
    AUTH_MESSAGE = 'authMessage'
    DATA_MESSAGE = 'dataMessage'
    RELAY_MESSAGE = 'relayMessage'
    SYNC_MESSAGE = 'syncMessage'


class AuthMessageType(Enum):
    """
    Functional types of auth messages
    """
    REQUEST = 'request'
    INVITE = 'invite'
    RESPONSE = 'response'
    JOIN = 'join'
    LEAVE = 'leave'
    STATUS = 'status'


class AuthMessageStatus(Enum):
    """
    Status of an auth message
    """
    SENT = 'sent'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class SyncTarget(Enum):
    """
    Types of target being synchronised over this message
    """
    NODE = 'node'
    USER = 'user'
    INDEX = 'index'
    INSTANCE = 'instance'
    FULL_SYNC = 'fullSync'
    POLL = 'poll'


class DataMessageType(Enum):
    """
    Types of data messages
    """
    QUERY = 'query'
    RESPONSE = 'response'
