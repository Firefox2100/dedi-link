from typing import TypeVar, Generic

from dedi_link.etc.enums import SyncTarget
from dedi_link.etc.exceptions import MessageAlreadyProcessed, NetworkMessageNotFound, NodeNotFound, \
    NetworkInterfaceException
from .. import NetworkMessageT
from ..network_message.network_message_header import NetworkMessageHeader, NetworkMessageHeaderT
from ..network_message.network_relay_message import NetworkRelayMessage, NetworkRelayMessageT
from ..network_message.network_sync_message import NetworkSyncMessage, NetworkSyncMessageT
from ..network import NetworkT
from ..node import Node, NodeT
from ..user import User
from ..data_index import DataIndex, DataIndexT
from ..user_mapping import UserMappingT
from .network_interface import NetworkInterface


class RelayInterface(NetworkInterface[
                         NetworkT,
                         NodeT,
                         NetworkMessageHeaderT,
                         NetworkRelayMessageT,
                         DataIndexT,
                         UserMappingT
                     ],
                     Generic[
                         NetworkT,
                         NodeT,
                         NetworkMessageHeaderT,
                         NetworkRelayMessageT,
                         DataIndexT,
                         UserMappingT
                     ]
                     ):
    def receive_message(self,
                        message: NetworkMessageT,
                        headers: NetworkMessageHeaderT,
                        should_raise: bool = False,
                        ) -> NetworkMessageT | None:
        """
        The general interface to receive a relay message and act upon it

        :param message: The relay message to process
        :param headers: The headers of the message
        :param should_raise: Whether to raise exceptions or return them
        """
        try:
            self.validate_message(
                message=message,
                headers=headers,
            )

            # Check the database to see if this message has been processed
            try:
                # Check if the relay message with the same ID exists, because relay message may have async responses
                stored_message = NetworkRelayMessage.load(message.message_id)

                # There is indeed an original message, see if it's the recipient sending a response
                original_recipients = []
                for relay_target in stored_message.relay_targets:
                    original_recipients.extend(relay_target.recipient_ids)
                original_recipients = list(set(original_recipients))

                if message.sender_id not in original_recipients:
                    # The sender is not the original recipients, the message is not a response
                    raise MessageAlreadyProcessed(f'Relay message {message.message_id} already processed')
            except NetworkMessageNotFound:
                stored_message = None

            if stored_message is None:
                # Store the message into the database
                message.store()
            else:
                # The recipient apparently got the message somewhere else, so remove the recipient from the list
                stored_message.remove_recipient(message.sender_id)

            message_recipients = []
            for relay_target in stored_message.relay_targets:
                message_recipients.extend(relay_target.recipient_ids)
            message_recipients = list(set(message_recipients))

            # Check if this node itself is in the recipient list
            if self.instance_id in message_recipients:
                # Route the message to the primary interface
                response = super().receive_message(message.message, message.headers)
                message.remove_recipient(self.instance_id)

                # Some node used a relay message to contact this node, indicating this node is not directly reachable
                import dedi_link.etc.consts
                dedi_link.etc.consts.PUBLIC_REACHABLE = False
        except Exception as e:
            if should_raise:
                raise e
