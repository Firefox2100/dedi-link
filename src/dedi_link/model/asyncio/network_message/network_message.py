import json
from typing import TypeVar, Generic, Protocol, ClassVar, Type

from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ...network_message.network_message_header import NetworkMessageHeader, NetworkMessageHeaderT
from ...network_message.network_message import NetworkMessageBase
from ..base_model import AsyncDataInterface
from ..network import Network, NetworkT
from ..node import NodeT


NetworkMessageT = TypeVar('NetworkMessageT', bound='NetworkMessage')


class AsyncNetworkMessageBP(Protocol):
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


class AsyncNetworkMessageInterface(AsyncDataInterface,
                                   AsyncNetworkMessageBP,
                                   Generic[NetworkMessageHeaderT, NetworkT]
                                   ):
    @property
    async def signature(self) -> str:
        """
        Signature of the message payload

        :return: Signature in base64 encoded format
        """
        network = await self.NETWORK_CLASS.load(self.network_id)
        private_pem = await network.private_key
        payload = json.dumps(self.to_dict())

        return self._sign_payload(private_pem, payload)

    async def generate_headers(self,
                               access_token: str | None = None,
                               ) -> NetworkMessageHeaderT:
        """
        Generate the headers for the message

        :param access_token:
        :return: A NetworkMessageHeader instance
        """
        server_signature = await self.signature

        if access_token is None:
            access_token = await self.access_token

        return self.NETWORK_MESSAGE_HEADER_CLASS(
            node_id=self.node_id,
            network_id=self.network_id,
            server_signature=server_signature,
            access_token=access_token,
        )


class NetworkMessage(NetworkMessageBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                     AsyncNetworkMessageInterface,
                     Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                     ):
    NETWORK_CLASS = Network
