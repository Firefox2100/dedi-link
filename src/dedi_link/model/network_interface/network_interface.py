import math
import networkx as nx
from typing import TypeVar, Any, List
from collections import Counter
from contextlib import contextmanager

from dedi_link.etc.consts import LOGGER
from dedi_link.etc.exceptions import NetworkRequestFailed, NetworkInterfaceNotImplemented
from ..config import DDLConfig
from ..network import Network
from ..node import Node
from ..network_message import NetworkMessage, NetworkMessageHeader, NetworkMessageT
from .session import Session


T = TypeVar('T')
NetworkInterfaceT = TypeVar('NetworkInterfaceT', bound='NetworkInterface')


class NetworkInterface:
    def __init__(self,
                 network_id: str,
                 instance_id: str,
                 config: DDLConfig,
                 session: Session | None = None,
                 ):
        self.network_id = network_id
        self.instance_id = instance_id
        self.config = config

        if session is not None:
            self.session = session
        else:
            self.session = Session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def network_graph(self) -> nx.DiGraph:
        """
        Get a networkx.DiGraph representation of the network
        """
        raise NetworkInterfaceNotImplemented('network_graph method needs to be implemented by an application')

    def close(self):
        self.session.close()

    @classmethod
    def from_interface(cls,
                       interface: 'NetworkInterface',
                       ):
        """
        Factory method to create a new interface from an existing one
        """
        return cls(
            network_id=interface.network_id,
            instance_id=interface.instance_id,
            session=interface.session,
            config=interface.config,
        )

    @staticmethod
    def vote_from_responses(objects: List[List[T]], identifier: str, value_to_search: Any, obj_type=None) -> T:
        """
        Find the majority vote from a list of responses

        :param objects: List of responses, containing a list of objects
        :param identifier: Attribute to compare
        :param value_to_search: Value to search
        :param obj_type: Type of the object
        :return: Object that has the majority vote
        """
        # Create a list to store objects that match the identifier value
        matching_objects = []

        # Iterate through list[list[CustomClass]] to find objects that have the specified identifier value
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

    def check_connectivity(self,
                           url: str | None = None,
                           path: str = '/api'
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
        LOGGER.debug(f'Checking connectivity to {url}')

        if url is None:
            url = self.config.url + path
        else:
            # Ensure that this URL is different from the self URL
            if url == self.config.url + path:
                LOGGER.info('A URL check discovered a self-reference')

                return False

        # Check if URL contains "localhost" or "127.0.0.1"
        if 'localhost' in url or '127.0.0.1' in url:
            LOGGER.info('A URL check discovered a localhost reference')

            return False

        try:
            with Session() as session:
                response = session.get(url)
                return response['status'] == 'OK'
        except NetworkRequestFailed:
            return False
        except Exception as e:
            LOGGER.logger.debug(f'Connectivity check failed for {url}: {e}')
            return False

    def calculate_new_score(self,
                            time_elapsed: float,
                            record_count: int = None,
                            record_count_max: int = None,
                            ) -> float:
        if time_elapsed < 0:
            return -1.0

        response_time_score = max(-1.0, (30 - time_elapsed) / 30)

        if record_count is None:
            return response_time_score

        optimal_record_count = math.floor(self.config.optimal_record_percentage * record_count_max)

        if record_count <= record_count_max:
            sqr_param = (2 - (4 / optimal_record_count + 4 / (record_count_max - optimal_record_count)) *
                         optimal_record_count) / optimal_record_count ** 2

            sgl_param = 4 / optimal_record_count + 4 / (record_count_max - optimal_record_count)

            response_quality_score = sqr_param * record_count ** 2 + sgl_param * record_count - 1
        else:
            response_quality_score = (2 / (record_count_max - optimal_record_count) ** 2) * (record_count -
                                                                                             record_count_max) ** 2 - 1

        return self.config.time_score_weight * response_time_score + \
            (1 - self.config.time_score_weight) * response_quality_score

    def find_path_to_node(self,
                          node_id: str,
                          ) -> list[list[str]]:
        """
        Tries to find the shortest path to a node in the network
        """
        with self.network_graph as graph:
            # Find all shortest paths to the given node
            try:
                paths = nx.all_shortest_paths(graph, source=self.instance_id, target=node_id)
            except nx.NetworkXNoPath:
                # Not reachable, find the shortest path on all nodes that are reachable
                all_shortest_paths = nx.single_source_shortest_path(graph, source=self.instance_id)

                # Sort the paths by the score of the terminating node
                # Because nodes with higher scores are more likely to be able to reach other nodes
                paths = sorted(all_shortest_paths.items(), key=lambda x: graph.nodes[x[0]]['score'])

            # Compare them with scores
            max_score = -1
            best_path = None

            for path in paths:
                path_score = sum([graph.nodes[n]['score'] for n in path])

                if path_score > max_score:
                    max_score = path_score
                    best_path = path

            return [best_path]

    def send_message(self,
                           node: Node,
                           message: NetworkMessage,
                           path: str = '/api',
                           access_token: str | None = None,
                           should_raise: bool = False,
                           should_relay: bool = True,
                           ) -> tuple[NetworkMessage |
                                      None, NetworkMessageHeader | None]:
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
        LOGGER.debug(f'Sending message to {node.node_id} at {node.url}')

        target_reachable = self.check_connectivity(node.url + '/api')

        if target_reachable:
            url = node.url + path

            payload = message.to_dict()
            headers = message.generate_headers(
                access_token=access_token,
            ).headers

            start_time = time.monotonic()

            response = await self.session.post(url, json=payload, headers=headers)

            finish_time = time.monotonic()
            time_elapsed = finish_time - start_time

            record_count = None

            if message.message_type == NetworkMessageT.DATA_MESSAGE:
                message: NetworkDataMessage
                if message.data_type == NetworkDataMessageType.RECORD_QUERY:
                    # The response should be a record response
                    response_message, _ = await RecordDataResponse.from_response(response)
                    record_count = 0

                    for r in response_message.data:
                        record_count += r.record_count

            new_score = self.calculate_new_score(
                time_elapsed=time_elapsed,
                record_count=record_count,
                record_count_max=node.record_index.record_count or 0,
            )

            await node.update_score(new_score)

            if should_raise:
                response.raise_for_status()

            CvConfig().logger.debug(f'Message sent to {node.node_id} got response: {response.status}')
            if response.status != 200:
                CvConfig().logger.debug(f'Message: {payload}; Headers: {headers}')
                CvConfig().logger.debug(f'Response: {await response.text()}')

            CvConfig().logger.debug(f'Message type: {response.content_type}')
            CvConfig().logger.debug(f'Message body: {await response.text()}')

            if response.content_type == 'application/json':
                try:
                    response_message, response_message_header = await NetworkMessage.from_response(response)
                    json_response = await response.json()

                    CvConfig().logger.debug(f'Message sent to {node.node_id} got response: {json_response}')

                    try:
                        await self.validate_message(response_message, response_message_header, json_response['timestamp'])
                    except Exception as e:
                        if should_raise:
                            raise
                        else:
                            CvConfig().logger.debug(f'Validation failed for message sent to {node.node_id}: {e}')

                    return response_message, response_message_header
                except Exception as e:
                    CvConfig().logger.exception(f'Error parsing response: {e}')
                    return None, None
            else:
                return None, None
        elif should_relay:
            # Relay the message to the node
            CvConfig().logger.info(f'Node {node.node_id} is unreachable, relaying the message')

            relay_message = NetworkRelayMessage(
                sender_id=self.instance_id,
                recipient_ids=[node.node_id],
                headers=message.generate_headers(
                    network_id=self.network_id,
                    node_id=self.instance_id,
                    access_token=access_token,
                ),
                message=message,
            )

            response_message, response_message_header = await self.relay_message(
                message=relay_message,
                path=path,
                access_token=access_token,
                should_raise=should_raise,
                skipping_nodes=[node.node_id],
            )

            if response_message_header is not None:
                # Message routing successful, unpack the response
                assert isinstance(response_message, NetworkRelayMessage)

                return response_message.message, response_message.headers
        else:
            raise MessageUndeliverable('Message undeliverable')

    async def relay_message(self,
                            message: NetworkRelayMessage,
                            path: str = '/federation/federation/',
                            access_token: str | None = None,
                            should_raise: bool = False,
                            skipping_nodes: list[str] = None,
                            ) -> tuple[NetworkMessage | None, NetworkMessageHeader | None]:
        CvConfig().logger.debug(f'Relaying message in network {self.network_id}')

        network = await DiscoveryNetwork.load(self.network_id)
        nodes = await network.nodes_approved

        if skipping_nodes:
            # Remove the skipping nodes from the list
            nodes = [node for node in nodes if node.node_id not in skipping_nodes]

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
                CvConfig().logger.debug(f'Message {message.message_id} route succeeded via node {node.node_id}')
                return response_message, response_message_header

        return None, None

    @classmethod
    async def _validate_signature(cls,
                                  message: NetworkMessage,
                                  headers: NetworkMessageHeader,
                                  timestamp: int | None = None,
                                  ):
        """
        Validate the signature of a message from another node
        """
        vault = Vault()

        # Check the timestamp
        if timestamp is not None:
            # 1 minute tolerance
            if abs(timestamp - time.time()) > 60:
                CvConfig().logger.debug(f'Timestamp is not within tolerance: {timestamp} vs {time.time()}')

                raise InvalidTimestamp('Timestamp is not within tolerance')

        # Verify the signature
        signature = headers.server_signature
        node_id = headers.node_id
        network_id = headers.network_id

        if signature is None or node_id is None or network_id is None:
            raise InvalidSignature('Signature or node ID or network ID is missing')

        try:
            public_key = vault.get_node_key(network_id, node_id)
            vault.verify_signature(
                public_pem=public_key,
                signature=signature,
                payload=json.dumps(message.to_dict()),
            )
        except Exception as e:
            CvConfig().logger.debug(f'Signature verification failed: {signature}')
            CvConfig().logger.exception(e)

            raise InvalidSignature('Signature verification failed')

    @classmethod
    async def _validate_access_token(cls,
                                     message: NetworkMessage,
                                     headers: NetworkMessageHeader,
                                     ) -> str | None:
        keycloak = KeyCloak()
        access_token = headers.access_token

        if access_token is not None:
            try:
                node = await Node.load(headers.node_id)

                # See if the client ID matches with the node
                client_id = keycloak.get_client_id(
                    access_token=access_token,
                )
                if client_id != node.client_id:
                    raise InvalidAuthenticationStatus('Client ID mismatch')

                user_info = keycloak.get_user_info(
                    access_token=access_token,
                )

                # If the message is not data message, the user should be a service account
                if message.message_type != NetworkMessageT.DATA_MESSAGE:
                    if not user_info['preferred_username'].startswith('service-account-'):
                        raise InvalidAuthenticationStatus('Service account required')
                else:
                    # If the message is a data message, the user should be a normal user
                    if user_info['preferred_username'].startswith('service-account-'):
                        raise InvalidAuthenticationStatus('Service account not allowed')

                # Token validation passed, check if the node has authentication enabled
                if not node.authentication_enabled:
                    # Authentication is in place now
                    await node.update({'authenticationEnabled': True})

                user_id = user_info['sub']

                return user_id
            except InvalidAuthenticationStatus:
                # This error is not to be ignored
                raise
            except Exception as e:
                CvConfig().logger.debug(f'Access token validation failed: {access_token}, with {e}')
                CvConfig().logger.exception(e)
        else:
            raise InvalidAccessToken('Access token is missing')

    @classmethod
    async def _remap_user_from_message(cls,
                                       header: NetworkMessageHeader,
                                       ):
        keycloak = KeyCloak()
        node = await Node.load(header.node_id)

        if node.authentication_enabled:
            raise InvalidAuthenticationStatus('Authentication enabled but validation failed')

        try:
            subject_id = keycloak.validate_token_external(
                access_token=header.access_token,
                client_id=node.client_id,
            )
            user_id = node.user_mapping.remap(subject_id)
        except Exception as e:
            CvConfig().logger.exception(e)
            raise InvalidAuthenticationStatus('User mapping failed') from e

        return user_id

    @classmethod
    async def validate_message(cls,
                               message: NetworkMessage,
                               headers: NetworkMessageHeader,
                               timestamp: int | None = None,
                               validate_signature: bool = True,
                               validate_access_token: bool = True,
                               ) -> str:
        """
        Validate a message from another node.
        :param message: The message from the other node
        :param headers: The headers from the other node
        :param timestamp: The timestamp to check against; None to skip timestamp check
        :param validate_signature: Whether to validate the signature
        :param validate_access_token: Whether to validate the access token
        :return:
        """
        user_id = None

        if validate_signature:
            await cls._validate_signature(
                message=message,
                headers=headers,
                timestamp=timestamp,
            )

        # Validate the access token
        if validate_access_token:
            user_id = await cls._validate_access_token(
                message=message,
                headers=headers,
            )

        if user_id is None:
            # Access token authentication failed or skipped, remap the user
            user_id = await cls._remap_user_from_message(
                header=headers,
            )

        return user_id

    async def broadcast_message(self,
                                message: NetworkMessage,
                                path: str = '/federation/federation/',
                                access_token: str | None = None,
                                should_raise: bool = False,
                                skip_unreachable: bool = False,
                                change_id: bool = False,
                                skipping_nodes: List[str] = None,
                                ) -> List[tuple[NetworkMessage |
                                                NetworkSyncMessage, NetworkMessageHeader]]:
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
        CvConfig().logger.debug(f'Broadcasting message to all nodes in {self.network_id}')

        network = await DiscoveryNetwork.load(self.network_id)
        nodes = await network.nodes_approved

        if skipping_nodes:
            # Remove the skipping nodes from the list
            nodes = [node for node in nodes if node.node_id not in skipping_nodes]

        reachable_nodes = []
        unreachable_nodes = []

        for node in nodes:
            if await self.check_connectivity(node.url + '/federation/'):
                reachable_nodes.append(node)
            else:
                unreachable_nodes.append(node)

        CvConfig().logger.debug(f'{len(reachable_nodes)} nodes are reachable, '
                                    f'{len(unreachable_nodes)} nodes are unreachable')

        tasks = []

        for node in reachable_nodes:
            if change_id:
                message.message_id = str(uuid.uuid4())
            tasks.append(self.send_message(node, message, path, access_token, should_raise))

        if message.message_type != NetworkMessageT.RELAY_MESSAGE:
            relay_message = NetworkRelayMessage(
                sender_id=self.instance_id,
                recipient_ids=[node.node_id for node in unreachable_nodes],
                headers=message.generate_headers(
                    network_id=self.network_id,
                    node_id=self.instance_id,
                    access_token=access_token,
                ),
                message=message,
            )
        elif isinstance(message, NetworkRelayMessage):
            # Repack the relay message
            CvConfig().logger.debug(f'Repacking the relay message {message.message_id}, ttl={message.ttl}')

            relay_message: NetworkRelayMessage = message
        else:
            raise ValueError('Invalid message type')

        if not skip_unreachable:
            CvConfig().logger.debug(f'Sending relay message to {len(unreachable_nodes)} unreachable nodes')

            for node in unreachable_nodes:
                tasks.append(
                    self.send_message(
                        node=node,
                        message=relay_message,
                        path=path,
                        access_token=access_token,
                        should_raise=should_raise,
                        should_relay=False,  # Prevent infinite recursion
                    )
                )

        if len(unreachable_nodes) > 0:
            # In case any node cannot be reached, no matter what
            # Store the message as a special one
            CvConfig().logger.debug(f'Storing the relay message {relay_message.message_id} for polling')

            relay_message.message_id = f'p-{relay_message.message_id}'

            await relay_message.store()

        results = await asyncio.gather(*tasks, return_exceptions=True)

        responses = []

        for result in results:
            if isinstance(result, Exception):
                CvConfig().logger.error(f'Message broadcast failed: {result}')
                CvConfig().logger.error(f'Stack trace: {traceback.format_exception(result)}')

                if should_raise:
                    raise result
            elif isinstance(result, tuple):
                responses.append(result)

        return responses

    async def receive_message(self,
                              message: NetworkMessage | NetworkSyncMessage | NetworkRelayMessage |
                              NetworkAuthMessage | NetworkDataMessage,
                              headers: NetworkMessageHeader,
                              should_raise: bool = False,
                              ) -> Response | None:
        """
        The general interface to receive a message and act upon it
        :param message: The message to process
        :param headers: The headers of the message
        :param should_raise: Whether to raise an exception when something fails, or suppress all expected exceptions
        """
        from .auth_interface import AuthInterface
        from .sync_interface import SyncInterface
        from .relay_interface import RelayInterface
        from .data_interface import DataInterface

        try:
            CvConfig().logger.info(f'Received message {message.message_id} of type {message.message_type}')
            CvConfig().logger.debug(f'Message received: {message.to_dict()}')

            if isinstance(message, NetworkAuthMessage):
                auth_interface = AuthInterface.from_interface(self)
                result = await auth_interface.receive_message(
                    message=message,
                    headers=headers,
                    should_raise=should_raise,
                )
            elif isinstance(message, NetworkSyncMessage):
                sync_interface = SyncInterface.from_interface(self)
                result = await sync_interface.receive_message(
                    message=message,
                    headers=headers,
                    should_raise=should_raise,
                )
            elif isinstance(message, NetworkRelayMessage):
                relay_interface = RelayInterface.from_interface(self)
                result = await relay_interface.receive_message(
                    message=message,
                    headers=headers,
                    should_raise=should_raise,
                )
            elif isinstance(message, NetworkDataMessage):
                data_interface = DataInterface.from_interface(self)
                result = await data_interface.receive_message(
                    message=message,
                    headers=headers,
                    should_raise=should_raise,
                )
            else:
                raise ValueError(f'Unknown message type: {message.message_type}')

            CvConfig().logger.debug(f'Response is {result} of type {type(result)}')

            if isinstance(result, NetworkMessage):
                # A response is required immediately
                response = result.to_response(
                    network_id=self.network_id,
                    node_id=self.instance_id,
                )

                CvConfig().logger.info(f'Responding to message {message.message_id} with type {result.message_type}')
                CvConfig().logger.debug(f'Response: {result.to_dict()}')

                return response
        except Exception as e:
            CvConfig().logger.exception(f'Error processing message {message.message_id}: {e}')
            if should_raise:
                raise e
