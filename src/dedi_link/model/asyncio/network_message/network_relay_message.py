from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ...network_message.network_relay_message import NetworkRelayMessageBase
from ...network_message.network_relay_message import RelayTarget as RelayTargetB
from ..network import NetworkT
from ..node import NodeT
from .network_message import NetworkMessage


RelayTargetT = TypeVar('RelayTargetT', bound='RelayTarget')
NetworkRelayMessageT = TypeVar('NetworkRelayMessageT', bound='NetworkRelayMessage')


class RelayTarget(RelayTargetB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                  Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                  ):
    pass


class NetworkRelayMessage(NetworkRelayMessageBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                          NetworkMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                          Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                          ):
    pass
