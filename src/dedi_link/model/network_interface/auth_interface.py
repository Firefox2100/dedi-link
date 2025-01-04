"""
Auth Interface

This module provides the specialised interface for the
authentication and authorisation process of the network.
"""

import json
from typing import TypeVar, Generic

from dedi_link.etc.consts import LOGGER
from dedi_link.etc.enums import AuthMessageStatus, AuthMessageType, MappingType
from dedi_link.etc.exceptions import MessageAlreadyProcessed, NodeNotFound, NetworkNotFound, \
    NetworkMessageNotFound
from ..network_message.network_message_header import NetworkMessageHeader, NetworkMessageHeaderT
from ..network_message.network_auth_message import NetworkAuthMessage, AuthRequest, AuthInvite, AuthResponse, \
    AuthJoin, AuthLeave, AuthStatus
from ..network_message.network_relay_message import NetworkRelayMessageT
from ..network import NetworkT
from ..node import Node, NodeT
from ..data_index import DataIndexT
from ..user_mapping import UserMapping, UserMappingT
from .network_interface import NetworkInterface


AuthInterfaceT = TypeVar('AuthInterfaceT', bound='AuthInterface')


class AuthInterface(NetworkInterface[
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
                    ]):
    """
    Auth Interface

    This class provides the specialised interface for the
    authentication and authorisation process of the network.
    """

    USER_MAPPING_CLASS = UserMapping

    def validate_message(self,
                         message: NetworkAuthMessage,
                         headers: NetworkMessageHeader,
                         validate_signature: bool = True,
                         validate_access_token: bool = True,
                         ) -> str:
        """
        Validate a message from another node.

        :param message: The message from the other node
        :param headers: The headers from the other node
        :param validate_signature: Whether to validate the signature
        :param validate_access_token: Whether to validate the access token
        :return:
        """
        user_id = None

        if message.auth_type in {AuthMessageType.REQUEST, AuthMessageType.INVITE}:
            # The node is not in database yet, use the one in the incoming message
            if not isinstance(message, AuthRequest) and not isinstance(message, AuthInvite):
                raise ValueError('Invalid message type for request or invite')

            node = message.node
        else:
            node = self.NODE_CLASS.load(headers.node_id)

        if validate_signature:
            self._validate_signature(
                signature=headers.server_signature,
                payload=json.dumps(message.to_dict()).encode(),
                node_public_key=node.public_key,
                timestamp=message.timestamp,
            )

        # Validate the access token
        if validate_access_token:
            user_id = self._validate_access_token(
                node_client_id=node.client_id,
                node_idp=node.idp,
                access_token=headers.access_token,
            )

        if user_id is None:
            # Token from this node cannot be introspected or exchanged
            message.node.authentication_enabled = False
            message.node.user_mapping = self.USER_MAPPING_CLASS(
                mapping_type=MappingType.STATIC,
                static_id=f'node:{message.node.node_id}',
            )

            # Access token authentication skipped, remap the user
            user_id = node.user_mapping.map()
        else:
            # Token can be introspected, turn on authentication
            message.node.authentication_enabled = True

        return user_id

    def _receive_auth_request(self,
                              message: AuthRequest,
                              ):
        """
        Receive and process an Auth Request message

        This method will not respond to the message, as this is a
        human decision. It will validate the message and store it

        :param message: The Auth Request message to process
        :return:
        """
        # Check if the node is already in the network
        try:
            self.NODE_CLASS.load(message.node.node_id)

            message.status = AuthMessageStatus.ACCEPTED
            message.store()
        except NodeNotFound:
            message.status = AuthMessageStatus.PENDING
            message.store()

    def _receive_auth_invite(self,
                             message: AuthInvite,
                             ):
        """
        Receive and process an Auth Invite message

        :param message: The Auth Invite message to process
        :return:
        """
        # Check if the node is already in the network
        try:
            self.NETWORK_CLASS.load(message.network_id)

        except NetworkNotFound:
            pass

        # Create a placeholder network
        network = self.NETWORK_CLASS(
            network_id=message.network_id,
            network_name=f'pending:{message.network_id}',
            description=f'This is a placeholder for a pending network {message.network_id}',
        )

        network.store()

        # Store the message
        message.status = AuthMessageStatus.PENDING
        message.store()

    def _receive_auth_response(self,
                               message: AuthResponse,
                               ):
        """
        Receive and process an Auth Response message

        The Auth Response message may be responding to either a request
        or an invitation.

        :param message: The Auth Response message received
        :return:
        """
        from .sync_interface import SyncInterface

        sync_interface = SyncInterface.from_interface(
            interface=self,
        )

        try:
            previous_message = AuthRequest.load(message.message_id)

            if previous_message.status != AuthMessageStatus.SENT:
                raise MessageAlreadyProcessed('Message already processed')

            if message.approved:
                if message.node is None:
                    raise ValueError(
                        'Approved response must have a Node object to represent itself'
                    )

                previous_message.update_status(AuthMessageStatus.ACCEPTED)

                # There should already be a placeholder network
                network = self.NETWORK_CLASS.load(self.network_id)

                # Update the placeholder with actual data
                update_payload = message.network.to_dict()
                update_payload.pop('nodeIds', None)
                update_payload.pop('instanceId')

                network.update(update_payload)

                # Store the node into the approved set
                network.add_node(message.node)

                # Sync to the new node
                sync_interface.sync_node(message.node)

                # Sync with the rest of the network
                sync_interface.sync_users()
            else:
                previous_message.update_status(AuthMessageStatus.REJECTED)

                try:
                    network = self.NETWORK_CLASS.load(self.network_id)
                    network.delete()
                except NetworkNotFound:
                    pass
        except NetworkMessageNotFound as e:
            previous_message = AuthInvite.load(message.message_id)

            if previous_message.status != AuthMessageStatus.SENT:
                raise MessageAlreadyProcessed('Message already processed') from e

            if message.approved:
                if message.node is None:
                    raise ValueError(
                        'Approved response must have a Node object to represent itself'
                    ) from e

                previous_message.update_status(AuthMessageStatus.ACCEPTED)

                network = self.NETWORK_CLASS.load(self.network_id)
                # Store the node into the approved set
                network.add_node(message.node)

                # Sync to the new node
                sync_interface.sync_node(message.node)

                # Sync with the rest of the network
                sync_interface.sync_users()

                # Notify the network that a new node has joined
                join_message = AuthJoin(
                    network_id=self.network_id,
                    node_id=self.instance_id,
                    node=message.node,
                )
                self.broadcast_message(
                    message=join_message,
                    skipping_nodes=[message.node.node_id],
                )
            else:
                previous_message.update_status(AuthMessageStatus.REJECTED)

    def _receive_auth_join(self,
                           message: AuthJoin,
                           ):
        """
        Receive and process an Auth Join message

        Auth Join message indicates that a new node joined the network.
        The newly joined nodes need to be approved first before they can
        participate in the network.

        :param message: The Auth Join message to process
        """
        if message.node.node_id == self.instance_id:
            # Message broadcast to this node by mistake
            return

        network = self.NETWORK_CLASS.load(self.network_id)

        # See if the new node is already known
        try:
            self.NODE_CLASS.load(message.node.node_id)

            raise MessageAlreadyProcessed(f'Node {message.node.node_id} already known to this node')
        except NodeNotFound:
            pass

        # Store the node into the network as not approved
        message.node.approved = False
        network.add_node(message.node)

    def _receive_auth_leave(self,
                            message: AuthLeave,
                            ):
        """
        Receive and process an Auth Leave message

        Auth Leave message indicates that a node has left the network.

        :param message: The Auth Leave message to process
        """
        try:
            node = self.NODE_CLASS.load(message.node_id)
            network = self.NETWORK_CLASS.load(self.network_id)

            network.remove_node(node)
        except NodeNotFound as e:
            raise MessageAlreadyProcessed('Node already deleted') from e

    def _receive_auth_status(self,
                             message: AuthStatus,
                             ):
        previous_message = NetworkAuthMessage.load(message.message_id)

        if not isinstance(previous_message, AuthRequest) and \
            not isinstance(previous_message, AuthInvite):
            raise ValueError('The message to check is not a request or invite')

        if previous_message.status == AuthMessageStatus.PENDING:
            return AuthStatus(
                message_id=previous_message.message_id,
                network_id=previous_message.network_id,
                node_id=self.instance_id,
                status=AuthMessageStatus.PENDING,
            )

        if previous_message.status == AuthMessageStatus.ACCEPTED:
            network = self.NETWORK_CLASS.load(self.network_id)
            self_node = network.get_self_node()

            return AuthResponse(
                message_id=previous_message.message_id,
                approved=previous_message.status == AuthMessageStatus.PENDING,
                node=self_node,
                network=network,
            )

        if previous_message.status == AuthMessageStatus.REJECTED:
            return AuthResponse(
                message_id=previous_message.message_id,
                approved=False,
            )

    def receive_message(self,
                        message: NetworkAuthMessage,
                        headers: NetworkMessageHeader,
                        should_raise: bool = False,
                        ):
        """
        The general interface to receive an authentication message and act upon it

        :param message: The auth message to process
        :param headers: The headers of the message
        :param should_raise: Whether to raise exceptions or return them
        """
        try:
            self.validate_message(
                message=message,
                headers=headers,
            )

            if message.auth_type == AuthMessageType.REQUEST:
                if not isinstance(message, AuthRequest):
                    raise ValueError('Invalid message type for request')

                return self._receive_auth_request(message)

            if message.auth_type == AuthMessageType.INVITE:
                if not isinstance(message, AuthInvite):
                    raise ValueError('Invalid message type for invite')

                return self._receive_auth_invite(message)

            if message.auth_type == AuthMessageType.RESPONSE:
                if not isinstance(message, AuthResponse):
                    raise ValueError('Invalid message type for response')

                return self._receive_auth_response(message)

            if message.auth_type == AuthMessageType.JOIN:
                if not isinstance(message, AuthJoin):
                    raise ValueError('Invalid message type for join')

                return self._receive_auth_join(message)

            if message.auth_type == AuthMessageType.LEAVE:
                if not isinstance(message, AuthLeave):
                    raise ValueError('Invalid message type for leave')

                return self._receive_auth_leave(message)

            if message.auth_type == AuthMessageType.STATUS:
                if not isinstance(message, AuthStatus):
                    raise ValueError('Invalid message type for status')

                return self._receive_auth_status(message)

            raise ValueError(f'Unknown auth type: {message.auth_type}')
        except Exception as e:
            LOGGER.exception(
                'Error processing message {}: {}',
                message.message_id,
                e,
            )

            if should_raise:
                raise

    def request_to_join(self,
                        node_url: str,
                        ):
        """
        Request to join a network by sending a join request to a node.

        :param node_url: URL of the node to send the request to
        :return:
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        node = network.get_self_node()

        message = AuthRequest(
            network_id=self.network_id,
            node_id=self.instance_id,
            status=AuthMessageStatus.SENT,
            node=node,
            target_url=node_url,
        )

        target_node = self.NODE_CLASS(
            url=node_url,
            node_id='',
            node_name='',
            client_id='',
            idp='',
            description='',
        )

        self.send_message(
            node=target_node,
            message=message,
            should_relay=False,
        )

        message.store()

    def invite_to_join(self,
                       node_url: str,
                       ):
        """
        Invite a node to join a network.

        :param node_url: The URL of the node to invite
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        self_node = network.get_self_node()

        message = AuthInvite(
            network_id=self.network_id,
            node_id=self.instance_id,
            status=AuthMessageStatus.SENT,
            node=self_node,
            target_url=node_url,
            network=network,
        )
        message.store()

        self.send_message(
            node=self.NODE_CLASS(
                url=node_url,
                node_id='',
                node_name='',
                client_id='',
                idp='',
                description='',
            ),
            message=message,
            should_relay=False,
        )

    def poll_status(self,
                    message_id: str
                    ):
        """
        Check the status of a previously sent auth request or invite

        :param message_id: The message ID to check
        :return:
        """
        try:
            previous_message = AuthRequest.load(message_id)
        except NetworkMessageNotFound:
            previous_message = AuthInvite.load(message_id)

        message = AuthStatus(
            message_id=message_id,
            network_id=self.network_id,
            node_id=self.instance_id,
        )
        node = self.NODE_CLASS(
            url=previous_message.target_url,
            node_id='',
            node_name='',
            client_id='',
            idp='',
            description='',
        )

        result, result_header = self.send_message(
            node=node,
            message=message,
            should_relay=False,
        )

        if isinstance(result, AuthStatus):
            # Still pending, do nothing
            pass
        elif isinstance(result, AuthResponse):
            # Response received, process it
            self.receive_message(
                message=result,
                headers=result_header,
            )

    def notify_join(self,
                    node: Node
                    ):
        """
        Notify the others that a new node has joined the network
        :param node: The node that has joined
        :return:
        """
        message = AuthJoin(
            network_id=self.network_id,
            node_id=self.instance_id,
            node=node,
        )

        self.broadcast_message(
            message,
            skipping_nodes=[node.node_id],
        )

    def notify_leave(self):
        """
        Notify the others that this node is leaving the network.
        :return:
        """

        message = AuthLeave(
            node_id=self.instance_id,
            network_id=self.network_id,
        )

        self.broadcast_message(message)

    def process_auth_request(self,
                             message_id: str,
                             approved: bool,
                             ):
        """
        Approve or reject an auth request or invite

        :param message_id: The message ID to process
        :param approved: Whether to approve or reject the request
        """
        try:
            previous_message = AuthRequest.load(message_id)
        except NetworkMessageNotFound:
            previous_message = AuthInvite.load(message_id)

        network = self.NETWORK_CLASS.load(self.network_id)

        if previous_message.status != AuthMessageStatus.PENDING:
            raise MessageAlreadyProcessed('Message already processed')

        if approved:
            if previous_message.node.idp == self.config.idp:
                # Token introspection enabled
                previous_message.node.authentication_enabled = True
            else:
                # Token introspection disabled
                previous_message.node.authentication_enabled = False
                previous_message.node.user_mapping = self.USER_MAPPING_CLASS(
                    mapping_type=MappingType.STATIC,
                    static_id=f'node:{previous_message.node.node_id}',
                )

        if previous_message.auth_type == AuthMessageType.REQUEST:
            # Join request
            if approved:
                network.add_node(previous_message.node)

                self.notify_join(previous_message.node)
        elif previous_message.auth_type == AuthMessageType.INVITE:
            # Join invite
            if approved:
                # Invite approved, store the network info
                network_dict = previous_message.network.to_dict()
                network_dict.pop('nodeIds', None)
                network_dict.pop('instanceId')

                network.update(network_dict)
                network.add_node(previous_message.node)

        # Build the response
        if approved:
            auth_response = AuthResponse(
                message_id=previous_message.message_id,
                approved=True,
                node=network.get_self_node(),
                network=network,
            )
        else:
            auth_response = AuthResponse(
                message_id=previous_message.message_id,
                approved=False,
            )

        # Send the response
        self.send_message(
            node=previous_message.node,
            message=auth_response,
            should_relay=False,
        )

        # Update the message status
        previous_message.update_status(
            AuthMessageStatus.ACCEPTED if approved else AuthMessageStatus.REJECTED
        )
