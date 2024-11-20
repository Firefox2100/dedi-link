from enum import Enum


class MappingType(Enum):
    NO_MAPPING = 'noMapping'
    STATIC = 'static'
    DYNAMIC = 'dynamic'


class MessageType(Enum):
    AUTH_MESSAGE = 'authMessage'
    DATA_MESSAGE = 'dataMessage'
    RELAY_MESSAGE = 'relayMessage'
    SYNC_MESSAGE = 'syncMessage'


class AuthMessageType(Enum):
    REQUEST = 'request'
    INVITE = 'invite'
    RESPONSE = 'response'
    JOIN = 'join'
    LEAVE = 'leave'
    STATUS = 'status'


class AuthMessageStatus(Enum):
    SENT = 'sent'
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


class SyncTarget(Enum):
    NODE = 'node'
    USER = 'user'
    INDEX = 'index'
    INSTANCE = 'instance'
    FULL_SYNC = 'fullSync'
    POLL = 'poll'
