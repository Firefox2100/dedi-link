from typing import TypeVar
from .base_model import AsyncBaseModel
from ..data_index import DataIndexType
from ..user_mapping import UserMappingType
from ..node import Node as SyncNode


NodeType = TypeVar('NodeType', bound='Node')


class Node(AsyncBaseModel, SyncNode[DataIndexType, UserMappingType]):
    pass
