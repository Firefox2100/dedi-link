"""
Node Model
"""

from uuid import uuid4
from typing import Optional
from pydantic import Field, ConfigDict

from .base import JsonModel


class Node(JsonModel):
    """
    A node in a network

    A Node object represents a node in the network, a basic
    unit of operation and communication.
    """
    model_config = ConfigDict(
        serialize_by_alias=True,
    )

    node_id: str = Field(
        default_factory=lambda: str(uuid4()),
        alias='nodeId',
        description='The unique ID of the node'
    )
    node_name: str = Field(
        ...,
        alias='nodeName',
        description='The name of the node'
    )
    url: str = Field(
        ...,
        description='The URL of the node'
    )
    description: str = Field(
        ...,
        description='A description of the node'
    )
    public_key: Optional[str] = Field(
        default=None,
        alias='publicKey',
        description='The public key of the node, used for secure communication'
    )
    approved: bool = Field(
        default=False,
        description='Whether the node is approved for message exchange'
    )
