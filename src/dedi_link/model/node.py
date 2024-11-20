from typing import Generic, TypeVar

from .base_model import BaseModel
from .data_index import DataIndex, DataIndexType
from .user_mapping import UserMapping, UserMappingType


NodeType = TypeVar('NodeType', bound='Node')


class Node(BaseModel, Generic[DataIndexType, UserMappingType]):
    DATA_INDEX_CLASS = DataIndex
    USER_MAPPING_CLASS = UserMapping

    def __init__(self,
                 node_id: str,
                 node_name: str,
                 url: str,
                 description: str,
                 client_id: str,
                 authentication_enabled: bool | None = None,
                 user_mapping: UserMappingType | None = None,
                 public_key: str | None = None,
                 data_index: DataIndexType = None,
                 score: float = 0.0,
                 ):

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

    def __eq__(self, other: 'Node') -> bool:
        if not isinstance(other, Node):
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
    def from_dict(cls, payload: dict) -> NodeType:
        """
        Build an installation from a dictionary
        :param payload: Dictionary containing installation information
        :return:
        """
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
            'nodeID': self.node_id,
            'nodeName': self.node_name,
            'nodeUrl': self.url,
            'clientID': self.client_id,
            'nodeDescription': self.description,
        }

        if self.authentication_enabled is not None:
            payload['authenticationEnabled'] = self.authentication_enabled
        if self.user_mapping is not None and self.user_mapping.mapping_type != UserMappingType.NO_MAPPING:
            payload['userMapping'] = self.user_mapping.to_dict()
        if self.public_key is not None and key:
            payload['publicKey'] = self.public_key
        if self.data_index is not None:
            payload['dataIndex'] = self.data_index.to_dict()
        if self.score:
            payload['score'] = self.score

        return payload
