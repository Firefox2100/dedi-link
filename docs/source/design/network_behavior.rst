=================================
Network Behavior and Optimisation
=================================

This section of document explains the behavior of the protocol based on different network architecture, and the optimisations in place designed for these scenarios.


Sample architecture
===================


Consider the following network structure:

.. graphviz:: network_sample.dot
    :align: center
    :caption: A sample network structure including most possible node states

Within it:

* **Source** is the node where the request is originating, or the "self" node, from the perspective of the running protocol. From here, all descriptions are based on this node.
* **A** is a direct neighbor, with two-way connectivity.
* **B** is a direct neighbor, can be reached but can't contact the source.
* **C** is a direct neighbor, can't be reached but can contact the source.
* **D** requires 1 hops to reach, can be reached via `S -> B -> D`, but can only reach the source via `D -> C -> S`.
* **E** requires 1 hops to reach, can be reached via both `S -> B -> E` and `S -> A -> E`, but can only reach the source via `E -> A -> S`.
* **F** is a direct neighbor, can be reached but can't contact the source.
* **G** requires 1 hops via `S -> F -> G`, however it may also be reached with 2 hops, via `S -> F -> H -> G`.
* **H** requires 1 hops via `S -> F -> H`.
* **I** requires 2 hops via `S -> F -> H -> I`.
* **Z** is a node that is not reachable from the source. It may be free floating completely (behind a firewall and do not poll), or further away than the TTL so a message never propogates to it. By default, TTL is 3, so maximum 2 hops are allowed.


Network states, reachability and routing
========================================


Due to the various connectivity states, the protocol is desiged to adapt to different network topology and states. To efficiently deliver messages to nodes, the protocol need to find an optimal routing that is fast enough, and uses reasonable amount of resources to avoid congestion. However, this conflicts with the decentralised nature of the protocol, since there are no central registry to store the network topology and speed. Thus, a localised network structure inference is used to determine the network topology and states.

The reachability is categorised simply into reachable and unreachable. In reality, the reachability may not be symmetric, i.e. a node may be able to reach another node, but the other node may not be able to reach the first node. This may be because of NAT, firewall, or other restrictions/tunneling. Additionaly, to avoid infinite loops and save resources, the protocol mandates a maximum TTL (Time To Live) for message hops (*please note, this is different from the TTL in IP packets*). 

At the beginning of a transmission, a node will attempt to send the message directly to the recipient. If it goes through, the recipient is considered a neighbor. If not, the node will attempt to see if it knows about a route to the target node. If it doesn't have sufficient information, the message is sent to other nodes, ranked by their score (based on the assumption that the higher the score, the more likely the node is to have a route to the target). Once the deliver is successful, the node will know of a route to the target, and will store this information for future use.

However, as the protocol currently stands, it does not record the routing information, except for how many hops have been taken. As a result, when the response comes back, the node does not know how it reached the destination. This will be addressed in the future updates to the protocol.


Routing behavior and optimisation
=================================


To optimise the message delivery, the protocol aims to:

* Always use the shortest route to deliver the message. It's expected that the overhead of using an extra server, perform the cryptographic verification, contact the IdP, then calculate the optimal route on the relay server, is significantly higher than using a slower server. (In short, one slower server is better than two faster servers).
* If there are multiple routes to the same destination, the one with higher score is chosen. The scoring mechanism employed by the protocol considers network performance, response speed and data quality of the node, and is designed as an incentive for the nodes to perform better.
* If multiple messages are to be sent together, or if a message needs to be sent to multiple nodes, the protocol will attempt to batch the messages together, and involve as few nodes as possible. This is both to reduce the load on shared resources (like the IdP), and to evenly distribute the load on the network.
