from flask import Blueprint, request

from .models import Network


network_blueprint = Blueprint('network', __name__)
user_blueprint = Blueprint('user', __name__)
federation_blueprint = Blueprint('federation', __name__)


@network_blueprint.route('/', methods=['GET'])
def get_networks():
    networks = Network.load_all()

    return [n.to_dict() for n in networks]


@network_blueprint.route('/', methods=['POST'])
def create_network():
    payload = request.json

    network = Network.from_dict(payload)

    network.store()


@network_blueprint.route('/<network_id>', methods=['GET'])
def get_network(network_id):
    network = Network.load(network_id)

    return network.to_dict()


@network_blueprint.route('/<network_id>', methods=['PATCH'])
def update_network(network_id):
    payload = request.json

    network = Network.load(network_id)

    network.update(payload)


@network_blueprint.route('/<network_id>', methods=['DELETE'])
def delete_network(network_id):
    network = Network.load(network_id)

    network.delete()


@network_blueprint.route('/<network_id>/nodes', methods=['GET'])
def get_nodes(network_id):
    network = Network.load(network_id)

    pending = request.args.get('pending', None)

    if pending is None:
        nodes = network.nodes
    elif pending.lower() == 'true':
        nodes = network.nodes_pending
    else:
        nodes = network.nodes_approved

    return [n.to_dict() for n in nodes]
