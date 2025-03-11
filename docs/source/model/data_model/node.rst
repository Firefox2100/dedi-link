Node class
==========

In the system design, a "node" refers to a single instance of the software running on a machine. It is an abstract concept, as a running instance may present as different nodes in different networks. Each node has a unique identifier (even for the same server across different networks) and other information.

A node contains the following mandatory information, which must be configured by the node and presented during the registration process:

* nodeId: A unique identifier for the node. This is generated when creating or joining a network, and will remain unchanged until leaving the network.
* nodeName: A human-readable name for the node. This is usually configured programmatically by the implementer.
* url: The root URL of the node, which is used to access the node's API.
* description: A human-readable description of the node.
* client_id: The client ID used in OIDC authentication by this node. A node may have multiple client IDs in different authentication providers, or federate a query that comes from a different client ID; but all requests carrying a service account token should be authenticated by this client ID.

A node may also have the following optional information, they are usually generated in runtime, representing some operational status of the node:

* authenticationEnabled: A boolean value indicating whether the node can issue access tokens that can be introspected by this system. This field is ignored when syncing information about nodes, and is always determined locally.
* userMapping: A special data structure indicating how to map a user to a local user if the authentication is not enabled. This field is not sent to other nodes.
* publicKey: The public key used by this node for signing messages. This key will rotate periodically, and the system implementation should ensure that the old key is not deactivated immediately, until all nodes are synced with this new key.
* dataIndex: A special data structure representing the index of queryable data within this node. The other nodes rely on this information to compose the query and determine the message frequency, routes, etc.
* score: A locally calculated score indicating how good the connection and data quality are for this node.
* approved: A boolean value representing whether this system has approved communication with this node. If false, the node's key will be rejected by the system, essentially disabling the connection.

Synchronous API:
----------------

.. autoclass:: dedi_link.model.node.Node
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:

Asynchronous API:
-----------------

.. autoclass:: dedi_link.model.asyncio.node.Node
    :members:
    :undoc-members:
    :show-inheritance:
    :inherited-members:
