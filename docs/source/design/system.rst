=============
System Design
=============

Overall Requirements
====================

The library is intended to be a backbone of a data discovery system. The system is designed to meet the following requirements, which are critical for its successful deployment and operation in a scientific research environment focused on data discovery, particularly in the health data sector:

* **Scalability**: The system supports the addition of new nodes without requiring significant reconfiguration or downtime. It efficiently handles increasing nodes and data queries, ensuring that performance does not degrade as the network expands.

* **Security**: Given the sensitive nature of the data, the system implements robust security measures, including data encryption, secure authentication, and validation mechanisms, to protect against unauthorised access, data breaches, and other potential threats. (Part of the authentication design needs to be implemented by each system that uses this library, for example via OIDC).

* **Interoperability**: The system is compatible with various data discovery protocols and tools, as long as they follows the standard query-response structure. Systems such as GA4GH BEACON, and FAIR Data Point can all be incorporated, while Cafe Variome V3 uses this protocol natively.

* **Resilience**: The system is designed to handle network partitions, node failures, and other disruptions without compromising its overall functionality. It ensures continuous operation and data availability even in the face of such challenges.

* **Minimal Centralisation**: The system does not rely on centralised control, adhering to a decentralised architecture where each node operates independently and manages its resources and security. The protocol and implementation follows zero-trust principles.

* **Ease of Use**: The library provides easy-to-use API and utilities for developers to integrate the protocol into their systems, reducing the complexity of implementation and enabling rapid deployment.

* **Performance**: The system effectively handles incoming queries, ensuring that researchers can access and analyse data efficiently without significant delays.

Class Diagram
=============

.. uml:: class_diagram.puml
    :caption: Class Diagram

