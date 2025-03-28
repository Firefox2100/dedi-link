import time
import json
import uuid
import jwt
import networkx as nx
from copy import deepcopy
from typing import TypeVar, Generic, Type
from contextlib import asynccontextmanager

from dedi_link.etc.enums import MessageType
from dedi_link.etc.exceptions import NetworkRequestFailed, NetworkInterfaceNotImplemented, MessageUndeliverable, \
                                     MessageAccessTokenInvalid, NodeAuthenticationStatusInvalid
from ...network_interface.network_interface import NetworkInterfaceBase
from ...data_index import DataIndexT
from ...user_mapping import UserMappingT
from ...config import DdlConfig
from ..network import Network, NetworkT
from ..node import Node, NodeT
from ..network_message import NetworkMessage, NetworkMessageT, NetworkMessageHeader, NetworkMessageHeaderT, \
                              NetworkRelayMessage, NetworkRelayMessageT, RelayTarget, RelayTargetT
from .session import Session


NetworkInterfaceT = TypeVar('NetworkInterfaceT', bound='NetworkInterface')


class NetworkInterface(NetworkInterfaceBase[
                           NetworkT,
                           NodeT,
                           NetworkMessageHeaderT,
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
                       ],
                       ):
    SESSION_CLASS = Session[NetworkMessageT, NetworkMessageHeaderT]
    NETWORK_CLASS = Network[DataIndexT, UserMappingT, NodeT]
    NODE_CLASS = Node[DataIndexT, UserMappingT]
    RELAY_TARGET_CLASS = RelayTarget[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
    NETWORK_MESSAGE_CLASS = NetworkMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT]
    NETWORK_RELAY_MESSAGE_CLASS = NetworkRelayMessage[NetworkMessageHeaderT, NetworkT, DataIndexT, UserMappingT, NodeT, RelayTargetT]

    def __init__(self,
                 network_id: str,
                 instance_id: str,
                 session: Session | None = None,
                 ):
        super().__init__(
            network_id=network_id,
            instance_id=instance_id,
        )

        if session is not None:
            self.session: Session = session
        else:
            self.session: Session = self.SESSION_CLASS()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @property
    @asynccontextmanager
    async def network_graph(self) -> nx.DiGraph:
        """
        Get a networkx.DiGraph representation of the network
        """
        raise NetworkInterfaceNotImplemented('network_graph method needs to be implemented by an application')

    async def close(self):
        await self.session.close()

    @classmethod
    def from_interface(cls: Type[NetworkInterfaceT],
                       interface: NetworkInterfaceT,
                       ) -> NetworkInterfaceT:
        """
        Factory method to create a new interface from an existing one
        """
        return cls(
            network_id=interface.network_id,
            instance_id=interface.instance_id,
            session=interface.session,
        )

    async def check_connectivity(self,
                                 url: str | None = None,
                                 ) -> bool:
        """
        Check whether the URL is reachable from the current machine.

        Note that this can only check the connectivity from the current machine.
        For example, the node may appear online, but it may be behind a firewall or filter
        that this machine can access while the others cannot

        If there is specific method to make it reachable (like a custom DNS record),
        it might still not be reachable from the outside, even if this method returns True.
        :param url: URL to check, None to check for the current node
        :param path: Path to check
        :return:
        """
        url = self._check_connectivity_url(
            url=url,
        )

        if url is None:
            return False

        try:
            async with self.SESSION_CLASS() as session:
                response = await session.get(url)
                return response['status'] == 'OK'
        except NetworkRequestFailed:
            return False

    async def find_relay_nodes(self,
                               node_ids: list[str],
                               ) -> list[str]:
        """
        Tries to the optimal node to use for relaying a message
        """
        async with self.network_graph as graph:
            return self._find_relay_nodes(
                network_graph=graph,
                node_ids=node_ids,
            )

    async def validate_message(self,
                               message: NetworkMessage,
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
        node = await self.NODE_CLASS.load(headers.node_id)

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
                request_idp=headers.idp_iss,
                access_token=headers.access_token,
            )

        if user_id is None:
            if node.authentication_enabled:
                raise NodeAuthenticationStatusInvalid(
                    'Authentication enabled but validation failed'
                )

            # Access token authentication skipped, remap the user
            user_id = node.user_mapping.map()

        return user_id

    async def send_message(self,
                           node: NodeT,
                           message: NetworkMessage,
                           path: str = '/api',
                           access_token: str | None = None,
                           should_raise: bool = False,
                           should_relay: bool = True,
                           ) -> tuple[NetworkMessage | None, NetworkMessageHeader | None]:
        """
        Send a message to a node.

        :param node: Node to send the message to
        :param message: Message to send
        :param path: Path to send the message to
        :param access_token: A custom access token; if None, the service account token will be used
        :param should_raise: Whether to raise an exception if the request fails
        :param should_relay: Whether to relay the message if the node is unreachable
        :return:
        """
        target_reachable = await self.check_connectivity(node.url + '/api')

        if target_reachable:
            url = node.url + path

            start_time = time.monotonic()

            response_message, response_header = await self.session.post(
                url=url,
                message=message,
                access_token=access_token,
            )

            finish_time = time.monotonic()
            time_elapsed = finish_time - start_time

            record_count = None

            if message.message_type == MessageType.DATA_MESSAGE:
                # Data message
                # An instance will only actively send out a query
                record_count = response_message.record_count

            new_score = self.calculate_new_score(
                time_elapsed=time_elapsed,
                record_count=record_count,
                record_count_max=node.data_index.record_count or 0,
            )

            await node.update_score(new_score)

            await self.validate_message(response_message, response_header)

            return response_message, response_header
        elif should_relay:
            relay_message = self.NETWORK_RELAY_MESSAGE_CLASS(
                network_id=self.network_id,
                node_id=self.instance_id,
                relay_targets=[
                    self.RELAY_TARGET_CLASS(
                        recipient_ids=[node.node_id],
                        header=await message.generate_headers(
                            access_token=access_token,
                        ),
                        message=message,
                    ),
                ],
            )

            response_message, response_header = await self.relay_message(
                message=relay_message,
                path=path,
                access_token=access_token,
                should_raise=should_raise,
                skipping_nodes=[node.node_id],
            )

            if response_header is not None:
                # Message routing successful, unpack the response
                if not response_header.delivered:
                    raise MessageUndeliverable('Relaying failed')

                # This method is only used when relaying a message to a single node
                # So the response should only contain one relay target
                if len(response_message.relay_targets) != 1:
                    raise ValueError('Relay message got unexpected response length')

                return response_message.relay_targets[0].message, response_message.relay_targets[0].header
        else:
            raise MessageUndeliverable('No direct route to target node')

    async def relay_message(self,
                            message: NetworkRelayMessageT,
                            path: str = '/federation/federation/',
                            access_token: str | None = None,
                            should_raise: bool = False,
                            skipping_nodes: list[str] = None,
                            ) -> tuple[NetworkRelayMessageT | None, NetworkMessageHeaderT | None]:
        network = await self.NETWORK_CLASS.load(self.network_id)
        nodes = await network.nodes_approved

        target_nodes = set()
        for target in message.relay_targets:
            target_nodes.update(target.recipient_ids)

        # Find the optimal next hops
        relay_nodes = set(await self.find_relay_nodes(
            node_ids=list(target_nodes),
        ))
        existing_nodes = set([node.node_id for node in nodes])

        if skipping_nodes:
            hops = list(relay_nodes & existing_nodes - set(skipping_nodes))
        else:
            hops = list(relay_nodes & existing_nodes)

        nodes = [n for n in nodes if n.node_id in hops]

        # Because this only happens after a message sending failure,
        # there is no need to check connectivity again
        for node in nodes:
            # Send one after another because only one route is needed
            response_message, response_message_header = await self.send_message(
                node=node,
                message=message,
                path=path,
                access_token=access_token,
                should_raise=should_raise,
                should_relay=False,
            )

            if response_message_header.delivered:
                # Message routing succeeded
                if not isinstance(response_message, NetworkRelayMessage):
                    # Relay message should only be responded with another relay message
                    raise ValueError(f'Relay message got unexpected response type: {response_message.message_type}')

                return response_message, response_message_header

        return None, None

    async def broadcast_message(self,
                                message: NetworkMessage,
                                path: str = '/api',
                                access_token: str | None = None,
                                should_raise: bool = False,
                                skip_unreachable: bool = False,
                                change_id: bool = False,
                                skipping_nodes: list[str] = None,
                                ) -> dict[str, tuple[NetworkMessageT, NetworkMessageHeaderT]]:
        """
        Broadcast a message to all nodes in the network.

        :param message: The message to send
        :param path: The path to send the message to
        :param access_token: The access token to use; if None, the service account token will be used
        :param should_raise: Whether to raise an exception if the request fails
        :param skip_unreachable: Whether to skip unreachable nodes
        :param change_id: Whether to change the message ID when sending to different node
        :param skipping_nodes: IDs of nodes to skip
        :return: A list of responses as NetworkMessage and NetworkMessageHeader tuples
        """
        network = await self.NETWORK_CLASS.load(self.network_id)
        nodes = await network.nodes_approved

        if skipping_nodes:
            # Remove the skipping nodes from the list
            nodes = [node for node in nodes if node.node_id not in skipping_nodes]

        reachable_nodes = []
        unreachable_nodes = []

        for node in nodes:
            if await self.check_connectivity(node.url):
                reachable_nodes.append(node)
            else:
                unreachable_nodes.append(node)

        responses = {}

        for node in reachable_nodes:
            if change_id:
                message.message_id = str(uuid.uuid4())

            response = await self.send_message(
                node=node,
                message=message,
                path=path,
                access_token=access_token,
                should_raise=should_raise,
            )

            responses[node.node_id] = response

        if len(unreachable_nodes) > 0:
            if message.message_type != NetworkMessageT.RELAY_MESSAGE:
                relay_message = self.NETWORK_RELAY_MESSAGE_CLASS(
                    network_id=self.network_id,
                    node_id=self.instance_id,
                    relay_targets=[
                        self.RELAY_TARGET_CLASS(
                            recipient_ids=[node.node_id for node in unreachable_nodes],
                            header=await message.generate_headers(access_token),
                            message=message,
                        ),
                    ],
                )
            elif isinstance(message, NetworkRelayMessage):
                # Repack the relay message
                relay_message = self.NETWORK_RELAY_MESSAGE_CLASS(
                    network_id=self.network_id,
                    node_id=self.instance_id,
                    relay_targets=message.relay_targets,
                )
            else:
                raise ValueError('Invalid message type')

            polling_message = deepcopy(relay_message)
            polling_message.message_id = f'p-{polling_message.message_id}'

            await polling_message.store()

            if not skip_unreachable:
                response, response_header = await self.relay_message(
                    message=relay_message,
                    path=path,
                    access_token=access_token,
                    should_raise=should_raise,
                    skipping_nodes=[node.node_id for node in reachable_nodes],
                )

                if response_header.delivered:
                    for relay_target in response.relay_targets:
                        if self.instance_id in relay_target.recipient_ids:
                            responses[relay_target.message.node_id] = (relay_target.message, relay_target.header)

        return responses
