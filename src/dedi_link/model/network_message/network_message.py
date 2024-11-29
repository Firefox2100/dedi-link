"""
Network Message Base classes
"""

import uuid
import time
import json
import base64
from enum import Enum
from typing import TypeVar, Type, Callable, Generic, Protocol, ClassVar
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType, AuthMessageType, DataMessageType
from dedi_link.etc.exceptions import NetworkMessageNotImplemented
from ..base_model import BaseModel, SyncDataInterface
from ..network import Network, NetworkT
from .network_message_header import NetworkMessageHeader, NetworkMessageHeaderT


NetworkMessageBT = TypeVar('NetworkMessageBT', bound='NetworkMessageB')
NetworkMessageT = TypeVar('NetworkMessageT', bound='NetworkMessage')


class SyncNetworkMessageBP(Protocol):
    """
    Protocol promises for the SyncNetworkMessageInterface
    """
    NETWORK_MESSAGE_HEADER_CLASS: ClassVar[Type[NetworkMessageHeader]]
    NETWORK_CLASS: ClassVar[Type[Network]]

    network_id: str
    node_id: str

    def to_dict(self) -> dict:
        ...

    def _sign_payload(self,
                      private_pem: str,
                      payload: str,
                      ) -> str:
        ...


class NetworkMessageB(BaseModel, Generic[NetworkMessageHeaderT, NetworkT]):
    """
    Base class for a Network Message
    """
    NETWORK_MESSAGE_HEADER_CLASS = NetworkMessageHeader
    NETWORK_CLASS = Network

    def __init__(self,
                 message_type: MessageType,
                 network_id: str,
                 node_id: str,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        """
        Base model for a network message

        :param message_type: The type of message
        :param network_id: The network ID
        :param node_id: The node ID
        :param message_id: The message ID
        :param timestamp: The timestamp in seconds since epoch
        """
        self.message_type = message_type
        self.message_id = message_id or str(uuid.uuid4())
        self.network_id = network_id
        self.node_id = node_id
        self.timestamp = timestamp or int(time.time())

    def __eq__(self, other):
        if not isinstance(other, NetworkMessage):
            return NotImplemented

        return all([
            self.message_type == other.message_type,
            self.message_id == other.message_id,
            self.network_id == other.network_id,
            self.node_id == other.node_id,
            self.timestamp == other.timestamp,
        ])

    def __hash__(self):
        return hash((
            self.message_type,
            self.message_id,
            self.network_id,
            self.node_id,
            self.timestamp
        ))

    @classmethod
    def _child_mapping(cls
                       ) -> dict[Enum, tuple[Type[NetworkMessageT], Callable[[dict], Enum] | None]]:
        from .network_auth_message import NetworkAuthMessage
        from .network_sync_message import NetworkSyncMessage
        from .network_data_message import NetworkDataMessage
        from .network_relay_message import NetworkRelayMessage

        return {
            MessageType.AUTH_MESSAGE: (
                NetworkAuthMessage,
                lambda payload: AuthMessageType(payload['messageAttributes']['authType'])
            ),
            MessageType.SYNC_MESSAGE: (NetworkSyncMessage, None),
            MessageType.DATA_MESSAGE: (
                NetworkDataMessage,
                lambda payload: DataMessageType(payload['messageAttributes']['dataType'])
            ),
            MessageType.RELAY_MESSAGE: (NetworkRelayMessage, None),
        }

    def to_dict(self) -> dict:
        payload = {
            'messageType': self.message_type.value,
            MESSAGE_ATTRIBUTES: {
                'messageId': self.message_id,
                'networkId': self.network_id,
                'nodeId': self.node_id,
            },
            'timestamp': self.timestamp,
        }

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> NetworkMessageBT:
        """
        Build an instance from a dictionary

        The from_dict method is purposefully not implemented, because under
        no circumstances should you want to construct a base class of message.
        Each message must be of a specific type, and use the factory method
        from the child class
        :param payload: The data dictionary containing the instance data
        :return: An instance of the model
        """
        raise NetworkMessageNotImplemented('from_dict method not implemented')

    @classmethod
    def factory(cls, payload: dict):
        id_var = MessageType(payload['messageType'])

        return cls.factory_from_id(
            payload=payload,
            id_var=id_var,
        )

    @classmethod
    def _sign_payload(cls,
                      private_pem: str,
                      payload: str,
                      ):
        private_key = serialization.load_pem_private_key(
            private_pem.encode(),
            password=None,
            backend=default_backend()
        )

        signature = private_key.sign(
            payload.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return base64.b64encode(signature).decode()


class SyncNetworkMessageInterface(SyncDataInterface,
                                  SyncNetworkMessageBP,
                                  Generic[NetworkMessageHeaderT, NetworkT]
                                  ):
    @property
    def signature(self) -> str:
        """
        Signature of the message payload

        :return: Signature in base64 encoded format
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        private_pem = network.private_key
        payload = json.dumps(self.to_dict())

        return self._sign_payload(private_pem, payload)

    def generate_headers(self,
                         access_token: str | None = None,
                         ) -> NetworkMessageHeaderT:
        """
        Generate the headers for the message

        :param access_token:
        :return: A NetworkMessageHeader instance
        """
        server_signature = self.signature

        if access_token is None:
            access_token = self.access_token

        return self.NETWORK_MESSAGE_HEADER_CLASS(
            node_id=self.node_id,
            network_id=self.network_id,
            server_signature=server_signature,
            access_token=access_token,
        )


class NetworkMessage(NetworkMessageB[NetworkMessageHeaderT, NetworkT],
                     SyncNetworkMessageInterface[NetworkMessageHeaderT, NetworkT],
                     Generic[NetworkMessageHeaderT, NetworkT]
                     ):
    """
    A generic network message structure

    A message is a self-contained unit of communication used in the protocol.
    All communication between nodes is RESTful, so all messages need to state
    clearly who it's from, who it's intended for, what it does, and have all
    the data needed to perform the action.
    """
