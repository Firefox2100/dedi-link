import uuid
from enum import Enum
from typing import TypeVar, Type, Callable, TYPE_CHECKING

from dedi_link.etc.enums import DataMessageType, MessageType
from ..network_message import NetworkMessage

if TYPE_CHECKING:
    from dedi_link.model import NetworkMessageType

NetworkDataMessageType = TypeVar('NetworkDataMessageType', bound='NetworkDataMessage')


class NetworkDataMessage(NetworkMessage):
    def __init__(self,
                 network_id: str,
                 node_id: str,
                 data_type: DataMessageType,
                 data,
                 should_relay: bool,
                 message_id: str = None,
                 timestamp: int | None = None,
                 ):
        super().__init__(
            message_type=MessageType.DATA_MESSAGE,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.network_id = network_id
        self.node_id = node_id
        self.data_type = data_type
        self.data = data
        self.should_relay = should_relay

    @classmethod
    def _child_mapping(cls) -> dict[Enum, tuple[Type['NetworkMessageType'], Callable[[dict], Enum] | None]]:
        from .data_query import DataQuery
        from .data_response import DataResponse

        return {
            DataMessageType.QUERY: (DataQuery, None),
            DataMessageType.RESPONSE: (DataResponse, None),
        }

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload['messageAttributes'].update({
            'networkID': self.network_id,
            'nodeID': self.node_id,
            'dataType': self.data_type.value,
            'shouldRelay': self.should_relay,
        })

        payload['messageData'] = self.data

        return payload

    @staticmethod
    def _encrypt_payload(public_key: str,
                         payload: dict,
                         ) -> tuple[str, str, str, str]:
        raise NotImplementedError('NetworkDataMessage._encrypt_payload() must be implemented by subclasses')

    @staticmethod
    def _decrypt_payload(encrypted_key: str,
                         nonce: str,
                         auth_tag: str,
                         encrypted_payload: str,
                         public_key: str,
                         ) -> str:
        raise NotImplementedError('NetworkDataMessage._decrypt_payload() must be implemented by subclasses')
