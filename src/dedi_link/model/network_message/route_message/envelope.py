"""
RouteEnvelope class for routing messages in the network.

This class is used to wrap another message for routing purposes in a federated network.
"""

from typing import Literal
from pydantic import Field, ConfigDict

from dedi_link.etc.enums import MessageType
from ..network_message import NetworkMessage


class RouteEnvelope(NetworkMessage):
    """
    A message to envelope another message for proxy routing.
    """

    model_config = ConfigDict(
        extra='forbid',
        serialize_by_alias=True,
    )

    message_type: Literal[MessageType.ROUTE_ENVELOPE] = Field(
        MessageType.ROUTE_ENVELOPE,
        description='The type of the network message',
        alias='messageType',
    )
