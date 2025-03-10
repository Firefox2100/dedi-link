from dedi_link.model import DataIndex, UserMapping
from dedi_link.model.network_message import NetworkMessageHeader
from dedi_link.model.network_message import NetworkMessage as NetworkMessageLib

from ..network import Network
from ..node import Node


class NetworkMessage(NetworkMessageLib[
                         NetworkMessageHeader,
                         Network,
                         DataIndex,
                         UserMapping,
                         Node
                     ]):
    NETWORK_CLASS = Network
