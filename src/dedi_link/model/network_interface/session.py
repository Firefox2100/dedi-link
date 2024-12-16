import httpx
from typing import TypeVar, Generic

from dedi_link.etc.exceptions import NetworkRequestFailed
from ..network_message import NetworkMessage, NetworkMessageT, NetworkMessageHeader, NetworkMessageHeaderT


SessionT = TypeVar('SessionT', bound='Session')


class Session(Generic[NetworkMessageT, NetworkMessageHeaderT]):
    NETWORK_MESSAGE_CLASS = NetworkMessage
    NETWORK_MESSAGE_HEADER_CLASS = NetworkMessageHeader

    def __init__(self):
        self._client = httpx.Client()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._client.close()

    def get(self,
            url: str,
            ) -> dict:
        try:
            response = self._client.get(url)

            if response.status_code != 200:
                raise NetworkRequestFailed(response.status_code)

            return response.json()
        except Exception as e:
            raise NetworkRequestFailed(e) from e

    def post(self,
             url: str,
             message: NetworkMessageT,
             access_token: str | None = None,
             ) -> tuple[NetworkMessageT | None, NetworkMessageHeaderT | None]:
        try:
            payload = message.to_dict()
            headers = message.generate_headers(
                access_token=access_token,
            ).headers

            response = self._client.post(
                url,
                json=payload,
                headers=headers,
            )

            if response.status_code != 200:
                raise NetworkRequestFailed(response.status_code)

            if response.headers.get('Content-Type') == 'application/json':
                response_payload = response.json()
                response_headers = response.headers

                response_message = self.NETWORK_MESSAGE_CLASS.factory(response_payload)
                response_header = self.NETWORK_MESSAGE_HEADER_CLASS.from_headers(response_headers)

                return response_message, response_header
            else:
                return None, None
        except Exception as e:
            raise NetworkRequestFailed(e) from e
