import uuid
from typing import TypeVar

from dedi_link.etc.enums import DataMessageType
from .network_data_message import NetworkDataMessage


DataQueryType = TypeVar('DataQueryType', bound='DataQuery')


class DataQuery(NetworkDataMessage):
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

        payload['messageAttributes']['userID'] = self.user_id

        return payload

    @classmethod
    def from_dict(cls, payload: dict) -> 'DataQuery':
        message_id = payload['messageAttributes']['messageID']
        network_id = payload['messageAttributes']['networkID']
        node_id = payload['messageAttributes']['nodeID']
        user_id = payload['messageAttributes']['userID']
        query = payload['messageData']

        return cls(
            message_id=message_id,
            network_id=network_id,
            node_id=node_id,
            user_id=user_id,
            query=query,
        )
