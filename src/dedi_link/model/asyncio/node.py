from typing import TypeVar
from .base_model import AsyncBaseModel
from ..data_index import DataIndexT
from ..user_mapping import UserMappingT
from ..node import Node as SyncNode


NodeT = TypeVar('NodeT', bound='Node')


class Node(SyncNode[DataIndexT, UserMappingT],
           AsyncBaseModel):
    pass
