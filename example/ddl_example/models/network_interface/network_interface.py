from dedi_link.model import DataIndex, UserMapping
from dedi_link.model.network_message import NetworkMessageHeader
from dedi_link.model.network_interface import NetworkInterface as NetworkInterfaceLib

from ..network import Network
from ..node import Node


class NetworkInterface(NetworkInterfaceLib[Network,
                           Node,
                           NetworkMessageHeader,
                           NetworkRelayMessageT,
                           DataIndex,
                           UserMapping
                       ]):

