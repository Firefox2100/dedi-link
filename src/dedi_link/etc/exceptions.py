class DeDiLinkException(Exception):
    pass


class DeDiLinkNotFoundException(DeDiLinkException):
    pass


class DeDiLinkNotImplementedException(DeDiLinkException, NotImplementedError):
    pass


class BaseModelNotImplementedException(DeDiLinkNotImplementedException):
    pass


class NetworkNotFoundException(DeDiLinkNotFoundException):
    pass


class NodeNotFoundException(DeDiLinkNotFoundException):
    pass
