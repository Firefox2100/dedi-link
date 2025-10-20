import time
from uuid import uuid4
from cryptography.hazmat.primitives.asymmetric import ec
import pytest

from dedi_link.model import Network, Node, Ec384PublicKey, Ec384PrivateKey, NetworkManagementKey


@pytest.fixture
def network_id():
    return uuid4()


@pytest.fixture
def node_id():
    return uuid4()


@pytest.fixture
def instance_id():
    return uuid4()


@pytest.fixture
def central_node():
    return uuid4()


@pytest.fixture
def message_id():
    return uuid4()


@pytest.fixture
def timestamp():
    return time.time()


@pytest.fixture
def ecdsa_p384_key_pair():
    private_key = ec.generate_private_key(
        curve=ec.SECP384R1(),
    )
    public_key = private_key.public_key()

    return private_key, public_key


@pytest.fixture
def private_key(ecdsa_p384_key_pair) -> Ec384PrivateKey:
    private_key, _ = ecdsa_p384_key_pair

    return Ec384PrivateKey(private_key)


@pytest.fixture
def public_key(ecdsa_p384_key_pair) -> Ec384PublicKey:
    _, public_key = ecdsa_p384_key_pair

    return Ec384PublicKey(public_key)


@pytest.fixture
def sample_network(network_id,
                   node_id,
                   instance_id,
                   central_node,
                   ) -> Network:
    return Network(
        networkId=network_id,
        networkName='Test Network',
        description='A test network for unit testing.',
        nodeIds=[node_id],
        visible=True,
        registered=True,
        instanceId=instance_id,
        centralNode=central_node,
    )


@pytest.fixture
def sample_node(node_id, public_key) -> Node:
    return Node(
        nodeId=node_id,
        nodeName='Test Node',
        url='https://testnode.example.com/api/.well-known/discovery-gateway',
        description='A test node for unit testing.',
        publicKey=public_key,
        approved=True,
    )


@pytest.fixture
def sample_management_key(private_key, public_key) -> NetworkManagementKey:
    return NetworkManagementKey(
        publicKey=public_key,
        privateKey=private_key,
    )
