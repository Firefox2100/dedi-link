Node class
==========

In the system design, a "node" refers to a single instance of the software running on a machine. It is an abstract concept, as a running instance may present as different nodes in different networks. Each node has a unique identifier (even for the same server across different networks) and other information.

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
