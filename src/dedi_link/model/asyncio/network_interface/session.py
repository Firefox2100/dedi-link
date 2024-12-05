from aiohttp import ClientSession
from typing import TypeVar, Generic

from dedi_link.etc.exceptions import NetworkRequestFailed
from ..network_message import NetworkMessageT, NetworkMessageHeader, NetworkMessageHeaderT


SessionT = TypeVar('SessionT', bound='Session')


class Session(Generic[NetworkMessageT, NetworkMessageHeaderT]):
    NETWORK_MESSAGE_HEADER_CLASS = NetworkMessageHeader

    def __init__(self):
        self._session = ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self._session.close()

    async def get(self,
                  url: str,
                  ) -> dict:
        response = await self._session.get(url)

        if response.status != 200:
            raise NetworkRequestFailed(response.status)

        return await response.json()

    async def post(self,
                   url: str,
                   message: NetworkMessageT,
                   access_token: str | None = None,
                   ) -> tuple[NetworkMessageT, NetworkMessageHeaderT]:
        payload = message.to_dict()

        headers = (await message.generate_headers(
            access_token=access_token,
        )).headers

        response = await self._session.post(
            url,
            json=payload,
            headers=headers,
        )

        if response.status != 200:
            raise NetworkRequestFailed(response.status)

        response_payload = await response.json()
        response_headers = response.headers

        response_message = message.factory(response_payload)
        response_header = NetworkMessageHeader.from_headers(response_headers)

        return response_message, response_header
