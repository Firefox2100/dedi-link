"""
This module contains the exceptions used in the decentralised discovery link.

They are separated into basic categories for easier catching and handling.
"""

class DeDiLinkException(Exception):
    """
    Base exception for all Decentralised Discovery Link exceptions.
    """


class DeDiLinkNotFound(DeDiLinkException):
    """
    Base exception for all resources not found errors
    """


class DeDiLinkNotImplemented(DeDiLinkException, NotImplementedError):
    """
    Base exception for all method not implemented (by this class or its parents) errors
    """


class BaseModelNotImplemented(DeDiLinkNotImplemented):
    """
    The called method is not implemented, which is defined in the base model.
    """


class NetworkNotFound(DeDiLinkNotFound):
    """
    The network was not found.
    """


class NetworkNotImplemented(DeDiLinkNotImplemented):
    """
    The called method is not implemented, which is defined in the network.
    """


class NodeNotFound(DeDiLinkNotFound):
    pass


class UserNotFound(DeDiLinkNotFound):
    pass


class UserNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkMessageNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkMessageNotFound(DeDiLinkNotFound):
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


class NetworkInterfaceException(DeDiLinkException):
    pass


class MessageSignatureInvalid(NetworkInterfaceException):
    pass


class MessageAccessTokenInvalid(NetworkInterfaceException):
    pass


class MessageTimestampInvalid(NetworkInterfaceException):
    pass


class MessageUndeliverable(NetworkInterfaceException):
    pass


class NodeAuthenticationStatusInvalid(NetworkInterfaceException):
    pass


class MessageAlreadyProcessed(NetworkInterfaceException):
    pass
