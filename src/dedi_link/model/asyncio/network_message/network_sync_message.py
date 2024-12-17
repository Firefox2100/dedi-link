from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ...network_message.network_sync_message import NetworkSyncMessageBase
from ..node import Node, NodeT
from ..network import NetworkT
from .network_message import NetworkMessage


NetworkSyncMessageT = TypeVar('NetworkSyncMessageT', bound='NetworkSyncMessage')


class NetworkSyncMessage(NetworkSyncMessageBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                         NetworkMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                         Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                         ):
    NODE_CLASS = Node
