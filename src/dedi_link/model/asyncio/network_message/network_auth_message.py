from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ...network_message.network_auth_message.network_auth_message import NetworkAuthMessageBase
from ...network_message.network_auth_message.auth_request import AuthRequestBase
from ...network_message.network_auth_message.auth_invite import AuthInviteBase
from ...network_message.network_auth_message.auth_response import AuthResponseBase
from ...network_message.network_auth_message.auth_join import AuthJoinBase
from ...network_message.network_auth_message.auth_leave import AuthLeaveBase
from ...network_message.network_auth_message.auth_status import AuthStatusBase
from ..node import Node, NodeT
from ..network import NetworkT
from .network_message import NetworkMessage


NetworkAuthMessageT = TypeVar('NetworkAuthMessageT', bound='NetworkAuthMessage')
AuthRequestT = TypeVar('AuthRequestT', bound='AuthRequest')
AuthInviteT = TypeVar('AuthInviteT', bound='AuthInvite')
AuthResponseT = TypeVar('AuthResponseT', bound='AuthResponse')
AuthJoinT = TypeVar('AuthJoinT', bound='AuthJoin')
AuthLeaveT = TypeVar('AuthLeaveT', bound='AuthLeave')
AuthStatusT = TypeVar('AuthStatusT', bound='AuthStatus')


class NetworkAuthMessage(NetworkAuthMessageBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                         NetworkMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                         Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                         ):
    pass


class AuthRequest(AuthRequestBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                  NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                  Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                  ):
    NODE_CLASS = Node


class AuthInvite(AuthInviteBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                 ):
    NODE_CLASS = Node


class AuthResponse(AuthResponseBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                   NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                   Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                   ):
    NODE_CLASS = Node


class AuthJoin(AuthJoinBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
               NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
               Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
               ):
    pass


class AuthLeave(AuthLeaveBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                ):
    pass


class AuthStatus(AuthStatusBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                 ):
    pass
