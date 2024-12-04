from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ..node import Node, NodeT
from ..network import NetworkT
from ...network_message.network_sync_message import NetworkSyncMessageB
from .network_message import NetworkMessage


NetworkSyncMessageT = TypeVar('NetworkSyncMessageT', bound='NetworkSyncMessage')


class NetworkSyncMessage(NetworkSyncMessageB[NetworkMessageHeaderT, NetworkT, NodeT],
                         NetworkMessage[NetworkMessageHeaderT, NetworkT],
                         Generic[NetworkMessageHeaderT, NetworkT, NodeT]
                         ):
    NODE_CLASS = Node
