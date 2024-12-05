from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ..network import NetworkT
from ...network_message.network_relay_message import NetworkRelayMessageB
from ...network_message.network_relay_message import RelayTarget as RelayTargetB
from .network_message import NetworkMessage


RelayTargetT = TypeVar('RelayTargetT', bound='RelayTarget')
NetworkRelayMessageT = TypeVar('NetworkRelayMessageT', bound='NetworkRelayMessage')


class RelayTarget(RelayTargetB[NetworkMessageHeaderT, NetworkT],
                  Generic[NetworkMessageHeaderT, NetworkT]
                  ):
    pass


class NetworkRelayMessage(NetworkRelayMessageB[NetworkMessageHeaderT, NetworkT, RelayTargetT],
                          NetworkMessage[NetworkMessageHeaderT, NetworkT],
                          Generic[NetworkMessageHeaderT, NetworkT, RelayTargetT]
                          ):
    pass
