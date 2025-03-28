"""
Network Interface Base Class

Network Interface is the core logic of the DediLink library, which provides the
decentralised and federated functions of communication and security.
"""

import math
import time
import uuid
import base64
import json
from collections import Counter
from copy import deepcopy
from contextlib import contextmanager
from typing import TypeVar, Any, List, Generic, Type

import networkx as nx
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from dedi_link.etc.consts import LOGGER
from dedi_link.etc.enums import MessageType
from dedi_link.etc.exceptions import MessageSignatureInvalid, MessageTimestampInvalid, \
    MessageAccessTokenInvalid, MessageUndeliverable, NodeAuthenticationStatusInvalid
from dedi_link.etc.exceptions import NetworkRequestFailed, NetworkInterfaceNotImplemented
from ..base_model import BaseModel
from ..network import Network, NetworkT
from ..node import Node, NodeT
from ..data_index import DataIndexT
from ..user_mapping import UserMappingT
from ..network_message import NetworkMessage, RelayTarget, NetworkRelayMessage, \
    NetworkMessageHeader, NetworkMessageT, NetworkRelayMessageT, NetworkMessageHeaderT
from .session import Session


T = TypeVar('T')
NetworkInterfaceBaseT = TypeVar('NetworkInterfaceBaseT', bound='NetworkInterfaceBase')
NetworkInterfaceT = TypeVar('NetworkInterfaceT', bound='NetworkInterface')


class NetworkInterfaceBase(BaseModel,
                           Generic[
                               NetworkT,
                               NodeT,
                               NetworkMessageHeaderT,
                               DataIndexT,
                               UserMappingT
                           ]):
    """
    Base class for Network Interface

    This class defines shared and concret methods used by all network
    interfaces, including the core logic of message validation,
    signature verification, and access token validation.
    """
    NETWORK_CLASS = Network[
        DataIndexT,
        UserMappingT,
        NodeT
    ]
    NODE_CLASS = Node[
        DataIndexT,
        UserMappingT
    ]
    RELAY_TARGET_CLASS = RelayTarget[
        NetworkMessageHeaderT,
        NetworkT,
        DataIndexT,
        UserMappingT,
        NodeT
    ]
    NETWORK_MESSAGE_CLASS = NetworkMessage[
        NetworkMessageHeaderT,
        NetworkT,
        DataIndexT,
        UserMappingT,
        NodeT
    ]
    NETWORK_RELAY_MESSAGE_CLASS = NetworkRelayMessage[
        NetworkMessageHeaderT,
        NetworkT,
        DataIndexT,
        UserMappingT,
        NodeT
    ]

    def __init__(self,
                 network_id: str,
                 instance_id: str,
                 ):
        """
        Network Interface Base Class

        :param network_id: The network ID this interface is bound to
        :param instance_id: The instance ID of this node within the network
        """
        self.network_id = network_id
        self.instance_id = instance_id

    @staticmethod
    def vote_from_responses(objects: List[List[T]],
                            identifier: str,
                            value_to_search: Any,
                            obj_type=None,
                            ) -> T:
        """
        Find the majority vote from a list of responses

        :param objects: List of responses, containing a list of objects
        :param identifier: Attribute to compare
        :param value_to_search: Value to search
        :param obj_type: Type of the object
        :return: Object that has the majority vote
        """
        # Create a list to store objects that match the identifier
        matching_objects = []

        # Iterate through list[list[CustomClass]] to find objects
        # that have the specified identifier value
        for sublist in objects:
            for obj in sublist:
                if obj_type is not None and isinstance(obj, dict):
                    o = obj_type.from_dict(obj)
                else:
                    o = obj
                if getattr(o, identifier) == value_to_search:
                    matching_objects.append(o)

        # Use Counter to find the most common object based on all its attributes
        counter = Counter(matching_objects)
        majority_object, _ = counter.most_common(1)[0]

        return majority_object

    def _check_connectivity_url(self,
                                url: str | None = None,
                                ) -> str | None:
        if url is None:
            url = self.config.url
        else:
            # Ensure that this URL is different from the self-URL
            if url == self.config.url:
                return None

        # Check if the URL contains "localhost" or "127.0.0.1"
        if 'localhost' in url or '127.0.0.1' in url:
            return None

        return url

    def _find_path_to_node(self,
                           network_graph: nx.DiGraph,
                           node_id: str,
                           route_through: list[str] | None = None,
                           route_length: int = None,
                           ) -> list[list[str]]:
        """
        Find the shortest path to a node in the network

        If there are no known paths to the node, return paths to all other nodes,
        ordered by the path score. This is based on the assumption that nodes with
        higher scores are more likely to be able to reach other nodes.

        :param network_graph: The network graph
        :param node_id: The node ID to find the path to
        :param route_through: Nodes that should be prioritised in the path. If present,
        the path will try to go through the nodes requested, as many as possible, unless
        there are shorter routes. These nodes override the score-based routing, but not
        the length-based routing.
        :param route_length: The maximum length of the route
        """
        try:
            paths = nx.all_shortest_paths(
                network_graph,
                source=self.instance_id,
                target=node_id,
            )

            # Compare them with scores
            max_score = -1
            max_going_through = -1
            best_path = None
            route_through = set(route_through) if route_through is not None else set()
            route_length = route_length or self.config.default_ttl + 1

            for path in paths:
                if len(path) > route_length:
                    # Path too long
                    continue

                path_score = sum([network_graph.nodes[n]['score'] for n in path])

                # See how many nodes are in the route_through list
                going_through = len(set(path) & route_through)

                if going_through > max_going_through:
                    best_path = path
                    max_going_through = going_through
                    max_score = path_score
                elif going_through == max_going_through:
                    if path_score > max_score:
                        best_path = path
                        max_score = path_score

            return [best_path] if best_path is not None else []
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            # Not reachable, find the shortest path on all nodes that are reachable
            all_shortest_paths = nx.single_source_shortest_path(
                network_graph,
                source=self.instance_id,
            )

            # Remove the path ending with the origin itself
            all_shortest_paths.pop(self.instance_id)

            # Sort the paths by the score of the terminating node, then by length
            # Because nodes with higher scores are more likely to be able to reach other nodes
            sorted_keys = sorted(
                all_shortest_paths.keys(),
                key=lambda x: (network_graph.nodes[x]['score'], -1 * len(all_shortest_paths[x])),
                reverse=True,
            )

            paths = [
                all_shortest_paths[k] for k in sorted_keys
                    if len(all_shortest_paths[k]) <= route_length
            ]

            return paths

    def _find_relay_nodes(self,
                          network_graph: nx.DiGraph,
                          node_ids: list[str],
                          ) -> list[str]:
        """
        Find a set of starting nodes that, once reached, can reach all the target nodes

        This is used to optimise the broadcasting feature, where if one node
        can reach multiple other nodes faster, it should be used as a common
        relaying point within the same request

        :param network_graph: The network graph
        :param node_ids: The node IDs to find the path to
        """
        starting_nodes = set()
        paths = []
        broadcast = False

        neighbors = list(network_graph.neighbors(self.instance_id))

        for node_id in node_ids:
            if node_id in neighbors:
                # Find the ones that can be delivered directly
                # These are the nodes that must appear in the final result
                starting_nodes.add(node_id)
            else:
                exist = False

                for path in paths:
                    if node_id in path:
                        # Already found a path to the node
                        exist = True
                        break

                if not exist:
                    shortest_paths = self._find_path_to_node(
                        network_graph=network_graph,
                        node_id=node_id,
                        route_through=list(starting_nodes) if starting_nodes else None,
                    )

                    if len(shortest_paths) == 0:
                        # Completely not reachable, skip this node
                        continue
                    elif len(shortest_paths) == 1:
                        # Routing found, add the path
                        paths.append(shortest_paths[0])
                    else:
                        # No direct path found, broadcast to all nodes
                        broadcast = True
                        break

        if broadcast:
            # Return all neighbours
            neighbors = sorted(
                neighbors,
                key=lambda x: network_graph.nodes[x]['score'],
                reverse=True,
            )

            return neighbors
        else:
            path_starting = [path[1] for path in paths]
            starting_nodes.update(path_starting)

            starting_list = list(starting_nodes)
            starting_list = sorted(
                starting_list,
                key=lambda x: network_graph.nodes[x]['score'],
                reverse=True,
            )

            return starting_list

    @classmethod
    def _validate_signature(cls,
                            signature: str,
                            payload: bytes,
                            node_public_key: str,
                            timestamp: int | None = None,
                            ):
        """
        Validate the signature of a message from another node
        """
        # Check the timestamp
        if timestamp is not None:
            # One minute tolerance
            if abs(timestamp - time.time()) > 60:
                raise MessageTimestampInvalid('Timestamp is not within tolerance')

        try:
            public_key = serialization.load_pem_public_key(
                node_public_key.encode(),
                backend=default_backend()
            )

            public_key.verify(
                base64.b64decode(signature),
                payload,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        except InvalidSignature:
            raise
        except Exception as e:
            raise MessageSignatureInvalid('Signature verification failed') from e

    def _validate_access_token(self,
                               node_client_id: str,
                               request_idp: str,
                               access_token: str,
                               ) -> str | None:
        """
        Validate the access token against the original OIDC IdP

        Note that this method decodes the token with the IdP's public key,
        so the signature is validated, but it does not send the token for
        introspection due to different implementation of the IdP connection.
        In this case, if the access token is revoked before it expires, it
        will still pass the validation.

        If your implementation of the library includes a connection to the IdP,
        consider using introspection instead.

        :param node_client_id: The client ID sender node uses
        :param request_idp: The IdP issuer of the access token
        :param access_token: The access token to validate
        :return: The user ID if the token is valid, None otherwise
        :raises MessageAccessTokenInvalid: If the token is invalid
        """
        try:
            introspect_result = self.oidc.introspect_token(
                token=access_token,
                driver_id=request_idp,
            )

            if not introspect_result['active']:
                raise MessageAccessTokenInvalid('Token is not active')

            if introspect_result['client_id'] != node_client_id:
                raise MessageAccessTokenInvalid('Client ID mismatch')

            return introspect_result['sub']
        except ValueError as e:
            raise MessageAccessTokenInvalid('Token issuer is not registered') from e
        except MessageAccessTokenInvalid:
            raise
        except Exception as e:
            LOGGER.warning('Token introspection failed: %s', e)
            return None

    def calculate_new_score(self,
                            time_elapsed: float,
                            record_count: int = None,
                            record_count_max: int = None,
                            ) -> float:
        """
        Calculate the new score of a node

        Calculation is based on the response time and quality.
        The response time is calculated based on the time elapsed
        from sending the request to receiving the response, with
        a maximum of 30 seconds. The response quality is calculated
        based on the record count of the response, with an optimal
        record count configurable of the maximum record count.
        """
        if time_elapsed < 0:
            return -1.0

        response_time_score = max(-1.0, (30 - time_elapsed) / 30)

        if record_count is None:
            return response_time_score

        optimal_record_count = math.floor(self.config.optimal_record_percentage * record_count_max)

        if record_count <= optimal_record_count:
            sqr_param = (2 - (4 / optimal_record_count + 4 /
                         (record_count_max - optimal_record_count)) *
                         optimal_record_count) / optimal_record_count ** 2

            sgl_param = 4 / optimal_record_count + 4 / (record_count_max - optimal_record_count)

            response_quality_score = sqr_param * record_count ** 2 + sgl_param * record_count - 1
        elif record_count <= record_count_max:
            response_quality_score = (2 / (record_count_max - optimal_record_count) ** 2) *\
                                     (record_count - record_count_max) ** 2 - 1
        else:
            raise ValueError('Record count exceeds maximum')

        return self.config.time_score_weight * response_time_score + \
            (1 - self.config.time_score_weight) * response_quality_score


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
                       ]):
    """
    Network Interface Class

    This class defines the methods used by the network interfaces
    to interact with the network, including sending and receiving
    messages, checking connectivity, and finding the optimal relay
    nodes for a message.
    """

    SESSION_CLASS = Session[NetworkMessageT, NetworkMessageHeaderT]

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    @contextmanager
    def network_graph(self) -> nx.DiGraph:
        """
        Get a networkx.DiGraph representation of the network
        """
        raise NetworkInterfaceNotImplemented(
            'network_graph method needs to be implemented by an application'
        )

    def close(self):
        """
        Close the session
        """
        self.session.close()

    @classmethod
    def from_interface(cls: Type[NetworkInterfaceT],
                       interface: 'NetworkInterface',
                       ) -> NetworkInterfaceT:
        """
        Factory method to create a new interface from an existing one
        """
        return cls(
            network_id=interface.network_id,
            instance_id=interface.instance_id,
            session=interface.session,
        )

    def check_connectivity(self,
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
            with self.SESSION_CLASS() as session:
                response = session.get(url)
                return response['status'] == 'OK'
        except NetworkRequestFailed:
            return False

    def find_relay_nodes(self,
                         node_ids: list[str],
                         ) -> list[str]:
        """
        Tries to find the optimal node to use for relaying a message

        :param node_ids: The node IDs to find the path to
        """
        with self.network_graph as graph:
            return self._find_relay_nodes(
                network_graph=graph,
                node_ids=node_ids,
            )

    def validate_message(self,
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

    def send_message(self,
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
        target_reachable = self.check_connectivity(node.url + '/api')

        if target_reachable:
            url = node.url + path

            start_time = time.monotonic()

            response_message, response_header = self.session.post(
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
                # so this should be a data response
                record_count = response_message.record_count

            if node.node_id != '':
                new_score = self.calculate_new_score(
                    time_elapsed=time_elapsed,
                    record_count=record_count,
                    record_count_max=node.data_index.record_count or 0,
                )

                node.update_score(new_score)

            self.validate_message(response_message, response_header)

            return response_message, response_header
        elif should_relay:
            relay_message = self.NETWORK_RELAY_MESSAGE_CLASS(
                network_id=self.network_id,
                node_id=self.instance_id,
                relay_targets=[
                    self.RELAY_TARGET_CLASS(
                        recipient_ids=[node.node_id],
                        route=[self.instance_id],
                        header=message.generate_headers(
                            access_token=access_token,
                        ),
                        message=message,
                    ),
                ],
            )

            response_message, response_header = self.relay_message(
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

                return (
                    response_message.relay_targets[0].message,
                    response_message.relay_targets[0].header
                )
        else:
            raise MessageUndeliverable('No direct route to target node')

    def relay_message(self,
                      message: NetworkRelayMessageT,
                      path: str = '/api',
                      access_token: str | None = None,
                      should_raise: bool = False,
                      skipping_nodes: list[str] = None,
                      ) -> tuple[NetworkRelayMessageT | None, NetworkMessageHeaderT | None]:
        """
        Relay a message to the next hop

        :param message: The message to relay
        :param path: The path to relay the message to
        :param access_token: The access token to use; if None,
            the service account token will be used
        :param should_raise: Whether to raise an exception if the request fails
        :param skipping_nodes: IDs of nodes to skip
        :return: The response message and header
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        nodes = network.nodes_approved

        target_nodes = set()
        for target in message.relay_targets:
            target_nodes.update(target.recipient_ids)

        # Find the optimal next hops
        relay_nodes = set(self.find_relay_nodes(
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
            response_message, response_message_header = self.send_message(
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
                    raise ValueError(
                        ('Relay message got unexpected response type:'
                         f'{response_message.message_type}')
                    )

                return response_message, response_message_header

        return None, None

    def broadcast_message(self,
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
        :param access_token: The access token to use; if None,
            the service account token will be used
        :param should_raise: Whether to raise an exception if the request fails
        :param skip_unreachable: Whether to skip unreachable nodes
        :param change_id: Whether to change the message ID when sending to different node
        :param skipping_nodes: IDs of nodes to skip
        :return: A dictionary of responses, with the node ID as the key
        """
        network = self.NETWORK_CLASS.load(self.network_id)
        nodes = network.nodes_approved

        if skipping_nodes:
            # Remove the skipping nodes from the list
            nodes = [node for node in nodes if node.node_id not in skipping_nodes]

        reachable_nodes = []
        unreachable_nodes = []

        for node in nodes:
            if self.check_connectivity(node.url):
                reachable_nodes.append(node)
            else:
                unreachable_nodes.append(node)

        responses = {}

        for node in reachable_nodes:
            if change_id:
                message.message_id = str(uuid.uuid4())

            response = self.send_message(
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
                            route=[self.instance_id],
                            header=message.generate_headers(access_token),
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
            polling_message.message_id = f'poll:{polling_message.message_id}'

            polling_message.store()

            if not skip_unreachable:
                response, response_header = self.relay_message(
                    message=relay_message,
                    path=path,
                    access_token=access_token,
                    should_raise=should_raise,
                    skipping_nodes=[node.node_id for node in reachable_nodes],
                )

                if response_header.delivered:
                    for relay_target in response.relay_targets:
                        if self.instance_id in relay_target.recipient_ids:
                            responses[relay_target.message.node_id] = \
                                (relay_target.message, relay_target.header)

        return responses

    def receive_message(self,
                        message: NetworkMessageT,
                        headers: NetworkMessageHeaderT,
                        should_raise: bool = False,
                        ) -> NetworkMessageT | None:
        """
        The general interface to receive a message and act upon it
        :param message: The message to process
        :param headers: The headers of the message
        :param should_raise: Whether to raise an exception when something fails, or suppress all expected exceptions
        """
        from .auth_interface import AuthInterface
        from .sync_interface import SyncInterface
        from .relay_interface import RelayInterface
        # from .data_interface import DataInterface

        try:
            if message.message_type == MessageType.AUTH_MESSAGE:
                auth_interface = AuthInterface.from_interface(self)
                result = auth_interface.receive_message(
                    message=message,
                    headers=headers,
                    should_raise=should_raise,
                )
            elif message.message_type == MessageType.SYNC_MESSAGE:
                sync_interface = SyncInterface.from_interface(self)
                result = sync_interface.receive_message(
                    message=message,
                    headers=headers,
                    should_raise=should_raise,
                )
            elif message.message_type == MessageType.RELAY_MESSAGE:
                relay_interface = RelayInterface.from_interface(self)
                result = relay_interface.receive_message(
                    message=message,
                    headers=headers,
                    should_raise=should_raise,
                )
            # elif message.message_type == MessageType.DATA_MESSAGE:
            #     data_interface = DataInterface.from_interface(self)
            #     result = data_interface.receive_message(
            #         message=message,
            #         headers=headers,
            #         should_raise=should_raise,
            #     )
            else:
                raise ValueError(f'Unknown message type: {message.message_type}')

            if isinstance(result, NetworkMessage):
                # A response is required immediately
                return result
        except Exception as e:
            LOGGER.exception('Error processing message: %s', e)

            if should_raise:
                raise
