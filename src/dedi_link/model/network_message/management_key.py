"""
A model to hold network management keys.
"""

from typing import Optional
from pydantic import Field, ConfigDict

from ..base import JsonModel


class NetworkManagementKey(JsonModel):
    """
    A model to hold network management keys.
    """
    model_config = ConfigDict(
        extra='forbid',
        serialize_by_alias=True,
    )

    public_key: str = Field(
        ...,
        description='The public key for the network management',
        alias='publicKey'
    )
    private_key: Optional[str] = Field(
        None,
        description='The private key for the network management',
        alias='privateKey'
    )
