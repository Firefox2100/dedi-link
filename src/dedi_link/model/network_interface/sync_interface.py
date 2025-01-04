from typing import TypeVar, Generic

from dedi_link.etc.enums import SyncTarget
from dedi_link.etc.exceptions import MessageAlreadyProcessed, NetworkMessageNotFound, NodeNotFound, \
    NetworkInterfaceException
from ..network_message.network_message_header import NetworkMessageHeader, NetworkMessageHeaderT
from ..network_message.network_relay_message import NetworkRelayMessage, NetworkRelayMessageT
from ..network_message.network_sync_message import NetworkSyncMessage, NetworkSyncMessageT
from ..network import NetworkT
from ..node import Node, NodeT
from ..user import User
from ..data_index import DataIndex, DataIndexT
from ..user_mapping import UserMappingT
from .network_interface import NetworkInterface


SyncInterfaceT = TypeVar('SyncInterfaceT', bound='SyncInterface')


class SyncInterface(NetworkInterface[
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
    NETWORK_SYNC_MESSAGE_CLASS = NetworkSyncMessage[
        NetworkMessageHeaderT,
        NetworkT,
        DataIndexT,
        UserMappingT,
        NodeT
    ]
    USER_CLASS = User
    DATA_INDEX_CLASS = DataIndex

    def _receive_user_sync(self,
                           message: NetworkSyncMessage,
                           ) -> NetworkSyncMessageT:
        """
        Receive a sync message for user data

        :param message: Message received from the node
        :return: Message to send back to the node
        """
        node = self.NODE_CLASS.load(message.node_id)

        for user_dict in message.data:
            node.store_user_key(
                user_id=user_dict['userId'],
                public_key=user_dict['publicKey'],
            )

        self_users = self.USER_CLASS.load_all()
        user_dicts = []

        for user in self_users:
            if ':' not in user.user_id:
                user_dicts.append({
                    'userId': user.user_id,
                    'publicKey': user.public_key,
                })

        return NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.USER,
            data=user_dicts,
            message_id=message.message_id,
        )

    def _receive_node_sync(self,
                           message: NetworkSyncMessage,
                           ) -> NetworkSyncMessage:
        """
        Receive a sync message for node data

        This method will only respond with nodes that has been approved by
        this instance. This is to prevent the ghosting of nodes, where a node
        has been evicted from the network but still has a record in the database.

        :param message: Message received from the node
        :return: Message to send back to the node
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        approved_nodes = network.nodes_approved

        # Remove the sender information
        approved_nodes = [node for node in approved_nodes if node.node_id != message.node_id]

        if message.data:
            for node_dict in message.data:
                node = self.NODE_CLASS.from_dict(node_dict)

                if node.node_id == self.instance_id:
                    continue

                try:
                    # Check if the node is already in the database
                    self.NODE_CLASS.load(node.node_id)
                except NodeNotFound:
                    # Not in the database
                    if node.node_id != self.instance_id:
                        network.add_node(node)

        return NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.NODE,
            data=[node.to_dict(key=True) for node in approved_nodes],
            message_id=message.message_id,
        )

    def _receive_instance_sync(self,
                               message: NetworkSyncMessage,
                               ) -> NetworkSyncMessage:
        """
        Receive a sync message for instance data

        This method is used to synchronise with an instance in the initial
        joining phase, or to confirm if some instance has been updated.

        :param message: Message received from the node
        :return: Message to send back to the node
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        self_node = network.get_self_node()

        if message.data:
            node = self.NODE_CLASS.from_dict(message.data[0])

            try:
                stored_node = self.NODE_CLASS.load(node.node_id)
                stored_node.update(node.to_dict())
            except NodeNotFound:
                network.add_node(node)

        return NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.INSTANCE,
            data=[self_node.to_dict(key=True)],
            message_id=message.message_id,
        )

    def _receive_index_sync(self,
                            message: NetworkSyncMessage,
                            ):
        """
        Receive a sync message for data index

        This method is used to synchronise the data index with other nodes

        :param message: Message received from the node
        :return: Message to send back to the node
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        node = self.NODE_CLASS.load(message.node_id)

        new_index = message.data[0]
        node.update_data_index(new_index)

        self_index = network.self_data_index

        response = NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.INDEX,
            data=[self_index],
            message_id=message.message_id,
        )

        return response

    def _receive_message_sync(self,
                              message: NetworkSyncMessage,
                              ):
        polling_messages = self.NETWORK_RELAY_MESSAGE_CLASS.load_polling()

        # Pop the node ID from the recipient list

        return NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.POLL,
            data=[polling_messages],
            message_id=message.message_id,
        )

    def receive_message(self,
                        message: NetworkSyncMessage,
                        headers: NetworkMessageHeader,
                        should_raise: bool = False,
                        ):
        """
        The general interface to receive a synchronisation message and act upon it

        :param message: The sync message to process
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
                self.NETWORK_SYNC_MESSAGE_CLASS.load(message.message_id)
                raise MessageAlreadyProcessed(f'Message {message.message_id} already processed')
            except NetworkMessageNotFound:
                pass

            # Store the message into the database
            message.store()

            if message.target_type == SyncTarget.USER:
                return self._receive_user_sync(message)

            if message.target_type == SyncTarget.NODE:
                return self._receive_node_sync(message)

            if message.target_type == SyncTarget.INSTANCE:
                return self._receive_instance_sync(message)

            if message.target_type == SyncTarget.INDEX:
                return self._receive_index_sync(message)

            if message.target_type == SyncTarget.FULL_SYNC:
                # TODO: Implement full sync
                return None

            if message.target_type == SyncTarget.POLL:
                return self._receive_message_sync(message)

            raise ValueError(f'Unknown sync target type: {message.target_type}')
        except Exception as e:
            if should_raise:
                raise e

    def sync_nodes(self):
        """
        Synchronize the member nodes in a network.
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        known_nodes = network.nodes_approved
        self_node = network.get_self_node()

        message = NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.NODE,
            data=[self_node.to_dict(key=True)],
        )

        # Broadcast the payload to all nodes
        results = self.broadcast_message(
            message=message,
            skip_unreachable=True,
            change_id=True,
        )

        # Find the difference between known nodes and reported nodes
        new_nodes = []
        updated_nodes = []

        for result, header in results:
            for node_dict in result.data:
                node = self.NODE_CLASS.from_dict(node_dict)
                if node.node_id in [n.node_id for n in known_nodes]:
                    # Node already known, check if there is any update
                    existing_node = next(e_node for e_node in known_nodes if e_node.node_id == node.node_id)

                    if node != existing_node:
                        if node.node_id in [n.node_id for n in updated_nodes]:
                            # Node is already in the updated list, skip
                            continue

                        # Node is different from recorded node.
                        # Contact the node directly to get the latest information and prevent ghost nodes
                        new_n = None

                        try:
                            message = NetworkSyncMessage(
                                network_id=self.network_id,
                                node_id=self.instance_id,
                                target_type=SyncTarget.INSTANCE,
                                data=[self_node.to_dict(key=True)],
                            )

                            response, _ = self.send_message(existing_node, message, should_relay=False)

                            assert isinstance(response, NetworkSyncMessage)

                            new_n = self.NODE_CLASS.from_dict(response.data[0])
                        except Exception:
                            pass

                        if new_n is None:
                            # Fetch failed, vote from the responses of other nodes
                            new_n = self.vote_from_responses(
                                objects=[result.data for result, _ in results],
                                identifier='node_id',
                                value_to_search=node.node_id,
                                obj_type=self.NODE_CLASS,
                            )

                        if new_n != existing_node:
                            updated_nodes.append(new_n)
                        else:
                            # Same as the recorded node, skip
                            continue
                    else:
                        # Same as the recorded node, skip
                        continue
                else:
                    # New node
                    if node.node_id in [n.node_id for n in new_nodes]:
                        # Node is already in the new list, skip
                        continue

                    # Vote from the majority as the new node has no record to work from
                    new_n = self.vote_from_responses(
                        objects=[result.data for result, _ in results],
                        identifier='node_id',
                        value_to_search=node.node_id,
                        obj_type=self.NODE_CLASS,
                    )

                    new_nodes.append(new_n)

        # Update the database records
        for node in updated_nodes:
            next(n for n in known_nodes if n.node_id == node.node_id).update(node.to_dict())

        # Add new nodes to the pending list
        for node in new_nodes:
            if node.node_id != self.instance_id:
                # Skip self
                node.approved = False
                network.add_node(node)

    def sync_node(self,
                  node: Node,
                  ):
        """
        Synchronise the node list with one node

        This is usually for initialisation, so this will accept
        all the known nodes reported by the target.

        :param node: The node to synchronise with
        """
        network = self.NETWORK_CLASS.load(self.network_id)

        message = NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.NODE,
            data=[(network.get_self_node()).to_dict(key=True)],
        )

        response, _ = self.send_message(node, message)

        if response is None:
            return
        else:
            if not isinstance(response, NetworkSyncMessage):
                raise NetworkInterfaceException('Message type error')

        for node_dict in response.data:
            n = self.NODE_CLASS.from_dict(node_dict)

            try:
                self.NODE_CLASS.load(n.node_id)
            except NodeNotFound:
                if n.node_id != self.instance_id:
                    # Prevent adding the node representing this instance
                    node.approved = False
                    network.add_node(n)

    def sync_users(self):
        """
        Synchronize the users list from other nodes in the network.
        :return:
        """
        self_users = self.USER_CLASS.load_all()
        users = [
            {
                'userId': user.user_id,
                'publicKey': user.public_key,
            } for user in self_users
        ]

        message = NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.USER,
            data=users,
        )

        # Broadcast the payload to all nodes
        results = self.broadcast_message(message)

        for node_id in results.keys():
            result, _ = results[node_id]
            node = self.NODE_CLASS.load(node_id)

            if isinstance(result, NetworkSyncMessage):
                for user in result.data:
                    node.store_user_key(
                        user_id=user['userId'],
                        public_key=user['publicKey'],
                    )

    def sync_index(self):
        """
        Synchronize the data index with other nodes in the network.
        """
        network = self.NETWORK_CLASS.load(self.network_id)

        self_index = network.self_data_index

        message = NetworkSyncMessage(
            network_id=self.network_id,
            node_id=self.instance_id,
            target_type=SyncTarget.INDEX,
            data=[self_index.to_dict()],
        )

        # Broadcast the payload to all nodes
        results = self.broadcast_message(message, change_id=True)

        for node_id in results.keys():
            result, _ = results[node_id]
            node = self.NODE_CLASS.load(node_id)

            if isinstance(result, NetworkSyncMessage):
                new_index = self.DATA_INDEX_CLASS.from_dict(result.data[0])

                node.update_data_index(new_index)

    def poll(self,
             node: Node | None = None,
             ):
        """
        Send a polling request to a node to fetch any message intended for this node

        :param node: The node to poll; if None, poll all nodes
        """
        network = self.NETWORK_CLASS.load(self.network_id)

        if node is not None:
            nodes = [node]
        else:
            nodes = network.nodes_approved

        def _send_poll_message(n: Node):
            message, headers = self.send_message(
                node=n,
                message=NetworkSyncMessage(
                    network_id=self.network_id,
                    node_id=self.instance_id,
                    target_type=SyncTarget.POLL,
                ),
            )

            if isinstance(message, NetworkSyncMessage):
                for message_dict in message.data:
                    m = NetworkRelayMessage.factory(message_dict)

                    # Remove the "p:" prefix
                    m.message_id = m.message_id.split(':')[1]

                    super().receive_message(m, headers)

        for node in nodes:
            _send_poll_message(node)
