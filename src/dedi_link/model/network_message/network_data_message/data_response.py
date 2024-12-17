import uuid
import json
from typing import TypeVar, Generic

from dedi_link.etc.enums import DataMessageType
from ...network import NetworkT
from ...node import Node, NodeT
from ...user import User
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ..network_message_header import NetworkMessageHeaderT
from .network_data_message import NetworkDataMessage, NetworkDataMessageBase


DataResponseBT = TypeVar('DataResponseBT', bound='DataResponseB')
DataResponseT = TypeVar('DataResponseT', bound='DataResponse')


class DataResponseB(NetworkDataMessageBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                    Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                    ):
    NODE_CLASS = Node
    USER_CLASS = User

    def __init__(self,
                 network_id: str,
                 node_id: str,
                 user_id: str,
                 responses: list[any],
                 message_id: str = None,
                 ):
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            data_type=DataMessageType.QUERY,
            data=responses,
            should_relay=True,
            message_id=message_id or str(uuid.uuid4()),
        )

        self.user_id = user_id

    @property
    def record_count(self) -> int:
        raise NotImplementedError

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload['messageAttributes']['userID'] = self.user_id

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> DataResponseBT:
        return cls(
            message_id=payload['messageAttributes']['messageId'],
            network_id=payload['messageAttributes']['networkId'],
            node_id=payload['messageAttributes']['nodeId'],
            user_id=payload['messageAttributes']['userId'],
            responses=payload['messageData'],
        )

    def encrypt(self) -> list[dict]:
        """
        Encrypt the responses with user public key

        :return: List of encrypted responses
        """
        network = self.NETWORK_CLASS.load(self.network_id)

        if self.node_id == network.instance_id:
            # The user is with this instance
            user = self.USER_CLASS.load(self.user_id)
            user_public_key = user.public_key
        else:
            node = self.NODE_CLASS.load(self.node_id)
            user_public_key = node.get_user_key(self.user_id)

        encrypted_responses = []

        for response in self.data:
            aes_key, nonce, auth_tag, encrypted_payload = self._encrypt_payload(
                user_public_key,
                response.to_dict()
            )

            encrypted_responses.append({
                'aesKey': aes_key,
                'nonce': nonce,
                'authTag': auth_tag,
                'encryptedPayload': encrypted_payload,
                'hash': response.sha256,
            })

        return encrypted_responses

    def decrypt(self, encrypted_responses: list[dict]) -> list[dict]:
        """
        Decrypt the responses with user private key

        :param encrypted_responses: List of encrypted responses
        :return: List of decrypted responses
        """
        decrypted_responses = []
        network = self.NETWORK_CLASS.load(self.network_id)

        if self.node_id == network.instance_id:
            # The user is with this instance
            user = self.USER_CLASS.load(self.user_id)
            user_public_key = user.public_key
        else:
            node = self.NODE_CLASS.load(self.node_id)
            user_public_key = node.get_user_key(self.user_id)

        for encrypted_response in encrypted_responses:
            response_str = self._decrypt_payload(
                encrypted_key=encrypted_response['aesKey'],
                nonce=encrypted_response['nonce'],
                auth_tag=encrypted_response['authTag'],
                encrypted_payload=encrypted_response['encryptedPayload'],
                public_key=user_public_key,
            )

            decrypted_responses.append(json.loads(response_str))

        return decrypted_responses


class DataResponse(DataResponseB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                   NetworkDataMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                   Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                   ):
    pass
