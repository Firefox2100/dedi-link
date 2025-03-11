"""
Network Message Header

This class is used to generate and parse headers for
network messages. There is usually no need to extend
this class.
"""

from typing import TypeVar, Type


NetworkMessageHeaderT = TypeVar('NetworkMessageHeaderT', bound='NetworkMessageHeader')


class NetworkMessageHeader:
    """
    Network Message Header

    This class is used to generate and parse headers for network messages.
    """
    def __init__(self,
                 node_id: str | None = None,
                 network_id: str | None = None,
                 server_signature: str | None = None,
                 idp_iss: str | None = None,
                 access_token: str | None = None,
                 user_id: str | None = None,
                 delivered: bool = False,
                 ):
        self.node_id = node_id
        self.network_id = network_id
        self.server_signature = server_signature
        self.idp_iss = idp_iss
        self.access_token = access_token
        self.user_id = user_id
        self.delivered = delivered

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented

        return all([
            self.node_id == other.node_id,
            self.network_id == other.network_id,
            self.server_signature == other.server_signature,
            self.idp_iss == other.idp_iss,
            self.access_token == other.access_token,
            self.user_id == other.user_id,
            self.delivered == other.delivered,
        ])

    def __hash__(self):
        return hash((
            self.node_id,
            self.network_id,
            self.server_signature,
            self.idp_iss,
            self.access_token,
            self.user_id,
            self.delivered,
        ))

    @property
    def headers(self) -> dict[str, str]:
        """
        A header dictionary for use in a request.
        """

        headers = {
            'Content-Type': 'application/json',
        }

        if self.node_id is not None:
            headers['X-Node-ID'] = self.node_id
        if self.network_id is not None:
            headers['X-Network-ID'] = self.network_id
        if self.server_signature is not None:
            headers['X-Server-Signature'] = self.server_signature
        if self.access_token is not None:
            headers['X-Issuer'] = self.idp_iss
            headers['Authorization'] = f'Bearer {self.access_token}'
        if self.user_id is not None:
            headers['X-User-ID'] = self.user_id
        if self.delivered is not None:
            headers['X-Delivered'] = 'true'

        return headers

    @classmethod
    def from_headers(cls: Type[NetworkMessageHeaderT], headers) -> NetworkMessageHeaderT:
        """
        Generate a NetworkMessageHeader object from a set of headers.
        :param headers: A header object that implements the get() method,
                        such as the headers from a Quart request object.
        :return: A NetworkMessageHeader object
        """
        access_token = headers.get('Authorization', None)
        idp_iss = headers.get('X-Issuer', None)
        if access_token is not None:
            access_token = access_token.split(' ')[1]

        if headers.get('X-Delivered', None) is not None:
            delivered = headers.get('X-Delivered', None).lower() == 'true'
        else:
            delivered = False

        return cls(
            node_id=headers.get('X-Node-ID', None),
            network_id=headers.get('X-Network-ID', None),
            server_signature=headers.get('X-Server-Signature', None),
            idp_iss=idp_iss,
            access_token=access_token,
            user_id=headers.get('X-User-ID', None),
            delivered=delivered,
        )
