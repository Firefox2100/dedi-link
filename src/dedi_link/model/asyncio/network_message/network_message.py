import json
from typing import TypeVar, Generic

from ..base_model import AsyncDataInterface
from ..network import Network, NetworkT
from ...network_message.network_message_header import NetworkMessageHeaderT
from ...network_message.network_message import NetworkMessageB


NetworkMessageT = TypeVar('NetworkMessageT', bound='NetworkMessage')


class NetworkMessage(NetworkMessageB[NetworkMessageHeaderT, NetworkT],
                     AsyncDataInterface,
                     Generic[NetworkMessageHeaderT, NetworkT],
                     ):
    NETWORK_CLASS = Network

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
