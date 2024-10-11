class DeDiLinkException(Exception):
    pass


class DeDiLinkNotFound(DeDiLinkException):
    pass


class DeDiLinkNotImplemented(DeDiLinkException, NotImplementedError):
    pass


class BaseModelNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkNotFound(DeDiLinkNotFound):
    pass


class NetworkNotImplemented(DeDiLinkNotImplemented):
    pass


class NodeNotFound(DeDiLinkNotFound):
    pass


class NetworkMessageNotImplemented(DeDiLinkNotImplemented):
    pass


class NetworkRelayMessageEnvelopeTooDeep(DeDiLinkException):
    pass


class NetworkRelayMessageNotAlive(DeDiLinkException):
    pass
