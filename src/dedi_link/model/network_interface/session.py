import requests

from dedi_link.etc.enums import MessageType
from dedi_link.etc.exceptions import NetworkRequestFailed
from ..network_message import NetworkMessageT, NetworkMessageHeader


class Session:
    def __init__(self):
        self._session = requests.Session()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def close(self):
        self._session.close()

    def get(self,
            url: str,
            ) -> dict:
        response = self._session.get(url)

        if response.status_code != 200:
            raise NetworkRequestFailed(response.status_code)

        return response.json()

    def post(self,
             url: str,
             message: NetworkMessageT,
             access_token: str | None = None,
             ) -> tuple[NetworkMessageT, NetworkMessageHeader]:
        payload = message.to_dict()
        headers = message.generate_headers(
            access_token=access_token,
        ).headers

        response = self._session.post(
            url,
            json=payload,
            headers=headers,
        )

        if response.status_code != 200:
            raise NetworkRequestFailed(response.status_code)

        response_payload = response.json()
        response_headers = response.headers

        message_type = MessageType(response_payload['messageType'])

        response_message = message.factory(response_payload, message_type)
        response_header = NetworkMessageHeader.from_headers(response_headers)

        return response_message, response_header
