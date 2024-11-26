"""
This module contains the exceptions used in the decentralised discovery link.

They are separated into basic categories for easier catching and handling.
"""

class DeDiLinkException(Exception):
    """
    Base exception for all Decentralised Discovery Link exceptions.
    """
    pass


class DeDiLinkNotFound(DeDiLinkException):
    """
    Base exception for all resources not found errors
    """
    pass


class DeDiLinkNotImplemented(DeDiLinkException, NotImplementedError):
    """
    Base exception for all method not implemented (by this class or its parents) errors
    """
    pass


class BaseModelNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkNotFound(DeDiLinkNotFound):
    pass


class NetworkNotImplemented(DeDiLinkNotImplemented):
    pass


class NodeNotFound(DeDiLinkNotFound):
    pass


class UserNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkMessageNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkRelayMessageEnvelopeTooDeep(DeDiLinkException):
    pass


class NetworkRelayMessageNotAlive(DeDiLinkException):
    pass


class NodeNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkInterfaceNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkRequestFailed(DeDiLinkException):
    pass
