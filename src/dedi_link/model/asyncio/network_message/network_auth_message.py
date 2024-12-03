from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ..node import Node, NodeT
from ..network import NetworkT
from ...network_message.network_auth_message.network_auth_message import NetworkAuthMessageB
from ...network_message.network_auth_message.auth_request_invite import AuthRequestInviteB
from ...network_message.network_auth_message.auth_response import AuthResponseB
from ...network_message.network_auth_message.auth_join import AuthJoinB
from ...network_message.network_auth_message.auth_leave import AuthLeaveB
from ...network_message.network_auth_message.auth_status import AuthStatusB
from .network_message import NetworkMessage


NetworkAuthMessageT = TypeVar('NetworkAuthMessageT', bound='NetworkAuthMessage')
AuthRequestInviteT = TypeVar('AuthRequestInviteT', bound='AuthRequestInvite')
AuthResponseT = TypeVar('AuthResponseT', bound='AuthResponse')
AuthJoinT = TypeVar('AuthJoinT', bound='AuthJoin')
AuthLeaveT = TypeVar('AuthLeaveT', bound='AuthLeave')
AuthStatusT = TypeVar('AuthStatusT', bound='AuthStatus')


class NetworkAuthMessage(NetworkAuthMessageB[NetworkMessageHeaderT, NetworkT],
                         NetworkMessage[NetworkMessageHeaderT, NetworkT],
                         Generic[NetworkMessageHeaderT, NetworkT]
                         ):
    pass


class AuthRequestInvite(AuthRequestInviteB[NetworkMessageHeaderT, NetworkT, NodeT],
                        NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                        Generic[NetworkMessageHeaderT, NetworkT, NodeT]
                        ):
    NODE_CLASS = Node


class AuthResponse(AuthResponseB[NetworkMessageHeaderT, NetworkT, NodeT],
                   NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                   Generic[NetworkMessageHeaderT, NetworkT, NodeT]
                   ):
    NODE_CLASS = Node


class AuthJoin(AuthJoinB[NetworkMessageHeaderT, NetworkT, NodeT],
               NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
               Generic[NetworkMessageHeaderT, NetworkT, NodeT]
               ):
    pass


class AuthLeave(AuthLeaveB[NetworkMessageHeaderT, NetworkT],
                NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                Generic[NetworkMessageHeaderT, NetworkT]
                ):
    pass


class AuthStatus(AuthStatusB[NetworkMessageHeaderT, NetworkT],
                 NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                 Generic[NetworkMessageHeaderT, NetworkT]
                 ):
    pass
