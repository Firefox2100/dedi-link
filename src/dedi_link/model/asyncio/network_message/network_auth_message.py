from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ..node import Node, NodeT
from ..network import NetworkT
from ...network_message.network_auth_message import NetworkAuthMessage as SyncNetworkAuthMessage
from ...network_message.network_auth_message import AuthRequestInvite as SyncAuthRequestInvite
from ...network_message.network_auth_message import AuthResponse as SyncAuthResponse
from ...network_message.network_auth_message import AuthJoin as SyncAuthJoin
from ...network_message.network_auth_message import AuthLeave as SyncAuthLeave
from ...network_message.network_auth_message import AuthStatus as SyncAuthStatus
from .network_message import NetworkMessage


NetworkAuthMessageT = TypeVar('NetworkAuthMessageT', bound='NetworkAuthMessage')
AuthRequestInviteT = TypeVar('AuthRequestInviteT', bound='AuthRequestInvite')
AuthResponseT = TypeVar('AuthResponseT', bound='AuthResponse')
AuthJoinT = TypeVar('AuthJoinT', bound='AuthJoin')
AuthLeaveT = TypeVar('AuthLeaveT', bound='AuthLeave')
AuthStatusT = TypeVar('AuthStatusT', bound='AuthStatus')


class NetworkAuthMessage(SyncNetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                         NetworkMessage[NetworkMessageHeaderT, NetworkT],
                         Generic[NetworkMessageHeaderT, NetworkT]
                         ):
    pass


class AuthRequestInvite(SyncAuthRequestInvite[NetworkMessageHeaderT, NetworkT, NodeT],
                        NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                        Generic[NetworkMessageHeaderT, NetworkT, NodeT]
                        ):
    NODE_CLASS = Node


class AuthResponse(SyncAuthResponse[NetworkMessageHeaderT, NetworkT, NodeT],
                   NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                   Generic[NetworkMessageHeaderT, NetworkT, NodeT]
                   ):
    NODE_CLASS = Node


class AuthJoin(SyncAuthJoin[NetworkMessageHeaderT, NetworkT, NodeT],
               NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
               Generic[NetworkMessageHeaderT, NetworkT, NodeT]
               ):
    pass


class AuthLeave(SyncAuthLeave[NetworkMessageHeaderT, NetworkT],
                NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                Generic[NetworkMessageHeaderT, NetworkT]
                ):
    pass


class AuthStatus(SyncAuthStatus[NetworkMessageHeaderT, NetworkT],
                 NetworkAuthMessage[NetworkMessageHeaderT, NetworkT],
                 Generic[NetworkMessageHeaderT, NetworkT]
                 ):
    pass
