"""
Node model
"""

from typing import Generic, TypeVar, Type

from dedi_link.etc.enums import MappingType
from dedi_link.etc.exceptions import NodeNotImplemented
from .base_model import BaseModel, SyncDataInterface
from .data_index import DataIndex, DataIndexT
from .user_mapping import UserMapping, UserMappingT


NodeBT = TypeVar('NodeBT', bound='NodeB')
NodeT = TypeVar('NodeT', bound='Node')


class NodeB(BaseModel, Generic[DataIndexT, UserMappingT]):
    """
    Base model for a Node
    """
    DATA_INDEX_CLASS = DataIndex
    USER_MAPPING_CLASS = UserMapping

    def __init__(self,
                 node_id: str,
                 node_name: str,
                 url: str,
                 description: str,
                 client_id: str,
                 authentication_enabled: bool | None = None,
                 user_mapping: UserMappingT | None = None,
                 public_key: str | None = None,
                 data_index: DataIndexT = None,
                 score: float = 0.0,
                 ):
        """
        A node in a network

        A Node object represents a node in the network, a basic
        unit of operation and communication.

        :param node_id: The unique ID of the node
        :param node_name: The name of the node
        :param url: The URL of the node
        :param description: A description of the node
        :param client_id: The client ID of the node
        :param authentication_enabled: Whether the requests coming from this node
        requires authentication. If disabled, all users will be mapped to the
        same static user with the same permissions.
        :param user_mapping: The user mapping for this node
        :param public_key: The public key of the node
        :param data_index: The data index of the node
        :param score: The score of the node
        """
        self.node_id = node_id
        self.node_name = node_name
        self.url = url
        self.public_key = public_key
        self.description = description
        self.authentication_enabled = authentication_enabled
        self.user_mapping = user_mapping
        self.client_id = client_id
        self.data_index = data_index or self.DATA_INDEX_CLASS()
        self.score = score

    def __eq__(self, other) -> bool:
        if not isinstance(other, NodeB):
            return NotImplemented

        return all([
            self.node_id == other.node_id,
            self.node_name == other.node_name,
            self.url == other.url,
            self.public_key == other.public_key,
            self.description == other.description,
            self.authentication_enabled == other.authentication_enabled,
            self.client_id == other.client_id,
        ])

    def __hash__(self) -> int:
        return hash(
            (
                self.node_id,
                self.node_name,
                self.url,
                self.public_key,
                self.description,
                self.authentication_enabled,
            )
        )

    @classmethod
    def from_dict(cls: Type[NodeBT], payload: dict) -> NodeBT:
        return cls(
            node_id=payload['nodeId'],
            node_name=payload['nodeName'],
            url=payload['nodeUrl'],
            client_id=payload['clientId'],
            description=payload.get('nodeDescription', ''),
            authentication_enabled=payload.get('authenticationEnabled', False),
            user_mapping=cls.USER_MAPPING_CLASS.from_dict(payload.get('userMapping', {})),
            public_key=payload.get('publicKey', None),
            data_index=cls.DATA_INDEX_CLASS.from_dict(payload.get('dataIndex', {})),
            score=payload.get('score', 0.0),
        )

    def to_dict(self, key=False) -> dict:
        payload = {
            'nodeId': self.node_id,
            'nodeName': self.node_name,
            'nodeUrl': self.url,
            'clientId': self.client_id,
            'nodeDescription': self.description,
        }

        if self.authentication_enabled is not None:
            payload['authenticationEnabled'] = self.authentication_enabled
        if (self.user_mapping is not None
                and self.user_mapping.mapping_type != MappingType.NO_MAPPING):
            payload['userMapping'] = self.user_mapping.to_dict()
        if self.public_key is not None and key:
            payload['publicKey'] = self.public_key
        if self.data_index is not None:
            payload['dataIndex'] = self.data_index.to_dict()
        if self.score is not None:
            payload['score'] = self.score

        return payload


class Node(NodeB[DataIndexT, UserMappingT],
           SyncDataInterface,
           Generic[DataIndexT, UserMappingT]
           ):
    """
    A node in a network

    A Node object represents a node in the network, a basic
    unit of operation and communication.
    """
    def get_user_key(self, user_id: str) -> str:
        """
        Get the user key for the given user ID

        This key is usually stored in KMS or similar service,
        and should not be held in memory for long. This is why
        it's not stored as a property of the Node object.

        :param user_id: The user ID to get the key for
        :return: The user key
        """
        raise NodeNotImplemented('get_user_key method not implemented')

    def update_score(self,
                     score: float,
                     ):
        """
        Wrapper method to update only the score of a node

        The score is updated with each request, so this method is
        more convenient to use than the update() method.

        :param score: New score to set
        :return:
        """
        self.update({
            'score': score,
        })
