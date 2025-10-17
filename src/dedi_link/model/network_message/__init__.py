from typing import Union, Annotated
from pydantic import Field

from .network_message import NetworkMessage
from .message_metadata import MessageMetadata
from .auth_message import AuthRequest, AuthInvite, AuthRequestResponse, AuthInviteResponse, \
    AuthConnect, AuthNotification
from .route_message import RouteRequest, RouteResponse, RouteNotification, RouteEnvelope
from .sync_message import SyncRequest, SyncNode
from .management_key import NetworkManagementKey


NetworkMessageUnion = Annotated[
    Union[
        AuthRequest,
        AuthInvite,
        AuthRequestResponse,
        AuthInviteResponse,
        AuthConnect,
        AuthNotification,
        RouteRequest,
        RouteResponse,
        RouteNotification,
        RouteEnvelope,
        SyncNode,
        SyncRequest,
    ],
    Field(
        description='Union type for network messages',
        discriminator='message_type',
    )
]
