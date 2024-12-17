import uuid
from typing import TypeVar, Generic

from dedi_link.etc.enums import DataMessageType
from ...network import NetworkT
from ...node import NodeT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ..network_message_header import NetworkMessageHeaderT
from .network_data_message import NetworkDataMessage, NetworkDataMessageBase


DataQueryBT = TypeVar('DataQueryBT', bound='DataQueryB')
DataQueryT = TypeVar('DataQueryT', bound='DataQuery')


class DataQueryB(NetworkDataMessageBase[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                 Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                 ):
    def __init__(self,
                 network_id: str,
                 node_id: str,
                 user_id: str,
                 query: any,
                 message_id: str = None,
                 ):
        super().__init__(
            network_id=network_id,
            node_id=node_id,
            data_type=DataMessageType.QUERY,
            data=query,
            should_relay=True,
            message_id=message_id or str(uuid.uuid4()),
        )

        self.user_id = user_id

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload['messageAttributes']['userId'] = self.user_id

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> DataQueryBT:
        return cls(
            message_id=payload['messageAttributes']['messageID'],
            network_id=payload['messageAttributes']['networkID'],
            node_id=payload['messageAttributes']['nodeID'],
            user_id=payload['messageAttributes']['userID'],
            query=payload['messageData'],
        )


class DataQuery(DataQueryB[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                NetworkDataMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT],
                Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                ):
    pass
