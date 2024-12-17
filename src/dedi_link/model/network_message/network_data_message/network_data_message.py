"""
Network Data Message

These messages are used to send data between nodes in a network.
"""

import uuid
from enum import Enum
from typing import TypeVar, Type, Callable, Generic

from dedi_link.etc.consts import MESSAGE_ATTRIBUTES
from dedi_link.etc.enums import DataMessageType, MessageType
from ...network import NetworkT
from ...node import NodeT
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ..network_message import NetworkMessageBase, NetworkMessage
from ..network_message_header import NetworkMessageHeaderT


NetworkDataMessageBaseT = TypeVar('NetworkDataMessageBaseT', bound='NetworkDataMessageBase')
NetworkDataMessageT = TypeVar('NetworkDataMessageT', bound='NetworkDataMessage')


class NetworkDataMessageBase(NetworkMessageBase[
                                 NetworkMessageHeaderT,
                                 NetworkT,
                                 DataIndexT,
                                 UserMappingT,
                                 NodeT
                             ],
                             Generic[
                                 NetworkMessageHeaderT,
                                 NetworkT,
                                 DataIndexT,
                                 UserMappingT,
                                 NodeT
                             ]):
    """
    Base class for Network Data Messages
    """
    message_type = MessageType.DATA_MESSAGE

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
            network_id=network_id,
            node_id=node_id,
            message_id=message_id or str(uuid.uuid4()),
            timestamp=timestamp,
        )

        self.data_type = data_type
        self.data = data
        self.should_relay = should_relay

    @classmethod
    def _child_mapping(cls) -> dict[Enum, tuple[Type[NetworkDataMessageBaseT],
                                    Callable[[dict], Enum] | None]]:
        from .data_query import DataQuery
        from .data_response import DataResponse

        return {
            DataMessageType.QUERY: (DataQuery, None),
            DataMessageType.RESPONSE: (DataResponse, None),
        }

    @classmethod
    def factory(cls: Type[NetworkDataMessageBaseT], payload: dict) -> NetworkDataMessageBaseT:
        id_var = DataMessageType(payload[MESSAGE_ATTRIBUTES]['dataType'])

        return cls.factory_from_id(
            payload=payload,
            id_var=id_var,
        )

    def to_dict(self) -> dict:
        payload = super().to_dict()

        payload['messageAttributes'].update({
            'dataType': self.data_type.value,
            'shouldRelay': self.should_relay,
        })

        payload['messageData'] = self.data

        return payload

    @staticmethod
    def _encrypt_payload(public_key: str,
                         payload: dict,
                         ) -> tuple[str, str, str, str]:
        raise NotImplementedError(
            'NetworkDataMessage._encrypt_payload() must be implemented by subclasses'
        )

    @staticmethod
    def _decrypt_payload(encrypted_key: str,
                         nonce: str,
                         auth_tag: str,
                         encrypted_payload: str,
                         public_key: str,
                         ) -> str:
        raise NotImplementedError(
            'NetworkDataMessage._decrypt_payload() must be implemented by subclasses'
        )


class NetworkDataMessage(NetworkDataMessageBase[
                             NetworkMessageHeaderT,
                             NetworkT,
                             DataIndexT,
                             UserMappingT,
                             NodeT
                         ],
                         NetworkMessage[
                             NetworkMessageHeaderT,
                             NetworkT,
                             DataIndexT,
                             UserMappingT,
                             NodeT
                         ],
                         Generic[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
                         ):
    pass
