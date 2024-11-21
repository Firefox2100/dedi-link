import uuid
import time
import json
import base64
from enum import Enum
from typing import TypeVar, Type, Callable, Generic
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import MessageType, AuthMessageType, DataMessageType
from dedi_link.etc.exceptions import NetworkMessageNotImplemented
from ..base_model import BaseModel
from ..network import Network
from .network_message_header import NetworkMessageHeader, NetworkMessageHeaderType


NetworkMessageType = TypeVar('NetworkMessageType', bound='NetworkMessage')


class NetworkMessage(BaseModel, Generic[NetworkMessageHeaderType]):
    """
    Base model for a network message

    A message is a self-contained unit of communication used in the protocol.
    All communication between nodes is RESTful, so all messages need to state
    clearly who it's from, who it's intended for, what it does, and have all
    the data needed to perform the action.
    """
    NETWORK_MESSAGE_HEADER_CLASS = NetworkMessageHeader

    def __init__(self,
                 message_type: MessageType,
                 network_id: str,
                 node_id: str,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
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
    def _child_mapping(cls) -> dict[Enum, tuple[Type[NetworkMessageType], Callable[[dict], Enum] | None]]:
        from .network_auth_message import NetworkAuthMessage
        from .network_sync_message import NetworkSyncMessage
        from .network_data_message import NetworkDataMessage
        from .network_relay_message import NetworkRelayMessage

        return {
            MessageType.AUTH_MESSAGE: (NetworkAuthMessage, lambda payload: AuthMessageType(payload['messageAttribute']['authType'])),
            MessageType.SYNC_MESSAGE: (NetworkSyncMessage, None),
            MessageType.DATA_MESSAGE: (NetworkDataMessage, lambda payload: DataMessageType(payload['messageAttribute']['dataType'])),
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
    def from_dict(cls, payload: dict) -> 'NetworkMessageType':
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

    @property
    def signature(self) -> str:
        """
        Signature of the message payload

        :return: Signature in base64 encoded format
        """
        network = Network.load(self.network_id)
        private_pem = network.private_key
        payload = json.dumps(self.to_dict())

        return self._sign_payload(private_pem, payload)

    def generate_headers(self,
                         access_token: str | None = None,
                         ) -> NetworkMessageHeaderType:
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
