"""
Node model
"""

from typing import Generic, TypeVar, Type

from dedi_link.etc.enums import MappingType
from dedi_link.etc.exceptions import NodeNotImplemented
from .base_model import BaseModel, SyncDataInterface
from .data_index import DataIndex, DataIndexT
from .user_mapping import UserMapping, UserMappingT


NodeBaseT = TypeVar('NodeBaseT', bound='NodeBase')
NodeT = TypeVar('NodeT', bound='Node')


class NodeBase(BaseModel,
               Generic[DataIndexT, UserMappingT]
               ):
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
                 *,
                 authentication_enabled: bool | None = None,
                 user_mapping: UserMappingT | None = None,
                 public_key: str | None = None,
                 data_index: DataIndexT = None,
                 score: float = 0.0,
                 approved: bool = False,
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
        :param approved: Whether the node is approved for message exchange
        """
        self.node_id = node_id
        self.node_name = node_name
        self.url = url
        self.public_key = public_key
        self.description = description
        self.authentication_enabled = authentication_enabled or False
        self.user_mapping = user_mapping or self.USER_MAPPING_CLASS()
        self.client_id = client_id
        self.data_index = data_index or self.DATA_INDEX_CLASS()
        self.score = score
        self.approved = approved

    def __eq__(self, other) -> bool:
        if not isinstance(other, NodeBase):
            return NotImplemented

        return all([
            self.node_id == other.node_id,
            self.node_name == other.node_name,
            self.url == other.url,
            self.public_key == other.public_key,
            self.description == other.description,
            self.authentication_enabled == other.authentication_enabled,
            self.client_id == other.client_id,
            self.approved == other.approved,
        ])

    def __hash__(self) -> int:
        return hash((
            self.node_id,
            self.node_name,
            self.url,
            self.public_key,
            self.description,
            self.authentication_enabled,
            self.client_id,
            self.approved,
        ))

    @classmethod
    def from_dict(cls: Type[NodeBaseT], payload: dict) -> NodeBaseT:
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
            approved=payload.get('approved', False),
        )

    def to_dict(self, key=False) -> dict:
        payload = {
            'nodeId': self.node_id,
            'nodeName': self.node_name,
            'nodeUrl': self.url,
            'clientId': self.client_id,
            'nodeDescription': self.description,
            'score': self.score,
            'approved': self.approved,
        }

        if self.authentication_enabled is not None:
            payload['authenticationEnabled'] = self.authentication_enabled
        if (self.user_mapping is not None
                and self.user_mapping.mapping_type != MappingType.NO_MAPPING):
            payload['userMapping'] = self.user_mapping.to_dict()
        if self.public_key is not None and key:
            payload['publicKey'] = self.public_key
        if self.data_index:
            payload['dataIndex'] = self.data_index.to_dict()

        return payload

    def _ema_score(self,
                   new_score: float,
                   ):
        """
        Calculate an updated score using Exponential Moving Average

        :param new_score: The new score to add
        :return: The updated score, considering both the previous and new scores
        """
        if self.score is None:
            return new_score

        weight = (self.config.ema_factor * (abs(new_score) / (abs(new_score) + abs(self.score))))
        return weight * new_score + (1 - weight) * self.score


class Node(NodeBase[DataIndexT, UserMappingT],
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

    def store_user_key(self, user_id: str, user_key: str):
        """
        Store the user key for the given user ID

        This key is usually stored in KMS or similar service,
        and should not be held in memory for long. This is why
        it's not stored as a property of the Node object.

        :param user_id: The user ID to store the key for
        :param user_key: The user key to store
        """
        raise NodeNotImplemented('store_user_key method not implemented')

    def update_score(self,
                     score: float,
                     ):
        """
        Wrapper method to update only the score of a node

        It calls the EMA calculation function to update the score

        :param score: New score to set
        :return:
        """
        new_score = self._ema_score(score)

        self.update({
            'score': new_score,
        })
