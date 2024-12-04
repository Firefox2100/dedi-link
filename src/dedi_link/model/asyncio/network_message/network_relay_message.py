from typing import TypeVar, Generic

from ...network_message.network_message_header import NetworkMessageHeaderT
from ..network import NetworkT
from ...network_message.network_relay_message import NetworkRelayMessageB
from .network_message import NetworkMessage


NetworkRelayMessageT = TypeVar('NetworkRelayMessageT', bound='NetworkRelayMessage')


class NetworkRelayMessage(NetworkRelayMessageB[NetworkMessageHeaderT, NetworkT],
                          NetworkMessage[NetworkMessageHeaderT, NetworkT],
                          Generic[NetworkMessageHeaderT, NetworkT]
                          ):
    pass
