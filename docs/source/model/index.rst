=============
System Models
=============

This section of the document explains the data models used in the system, the protocol, the library structure, and the data flow.

Data Models
===========

Considering different use cases, this library provides both synchronous and asynchronous interface on the API. This mainly concerns the database operation (which needs to be implemented by the developers who use this library) and the network operation (which is handled by the library itself). For other basic operations, all API are synchronous.

.. toctree::
    :maxdepth: 1

    data_model/user
    data_model/node
