from uuid import uuid4
from pydantic import Field, ConfigDict

from .base import JsonModel


class Network(JsonModel):
    """
    A network that contains nodes which agreed to share data among each other.

    A network is a logical abstraction of a group of nodes that accepts (partially)
    others' credentials and allows access to their data.
    """

    model_config = ConfigDict(
        serialize_by_alias=True,
    )

    network_id: str = Field(
        default_factory=lambda: str(uuid4()),
        alias='networkId',
        description='The unique ID of the network'
    )
    network_name: str = Field(
        ...,
        alias='networkName',
        description='The name of the network'
    )
    description: str = Field(
        default='',
        description='A description of the network'
    )
    node_ids: list[str] = Field(
        default_factory=list,
        alias='nodeIds',
        description='The IDs of the nodes in the network'
    )
    visible: bool = Field(
        default=False,
        description='Whether the network is visible to others to apply for joining'
    )
    registered: bool = Field(
        default=False,
        description='Whether the network is registered in a public registry'
    )
    instance_id: str = Field(
        default_factory=lambda: str(uuid4()),
        alias='instanceId',
        description='The unique ID of the network instance'
    )
    central_node: str | None = Field(
        default=None,
        alias='centralNode',
        description='The ID of the central node for permission and identity management. '
                    'None if the permission is decentralised.'
    )
