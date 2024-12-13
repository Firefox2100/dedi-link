from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ...network_message.network_auth_message.network_auth_message import NetworkAuthMessageB
from ...network_message.network_auth_message.auth_request import AuthRequestB
from ...network_message.network_auth_message.auth_invite import AuthInviteB
from ...network_message.network_auth_message.auth_response import AuthResponseB
from ...network_message.network_auth_message.auth_join import AuthJoinB
from ...network_message.network_auth_message.auth_leave import AuthLeaveB
from ...network_message.network_auth_message.auth_status import AuthStatusB
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


class NetworkAuthMessage(NetworkAuthMessageB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                         NetworkMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                         Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                         ):
    pass


class AuthRequest(AuthRequestB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                  NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                  Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                  ):
    NODE_CLASS = Node


class AuthInvite(AuthInviteB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                 ):
    NODE_CLASS = Node


class AuthResponse(AuthResponseB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                   NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                   Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                   ):
    NODE_CLASS = Node


class AuthJoin(AuthJoinB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
               NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
               Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
               ):
    pass


class AuthLeave(AuthLeaveB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                ):
    pass


class AuthStatus(AuthStatusB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 NetworkAuthMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                 ):
    pass
