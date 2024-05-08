---
title: 'Architecture Overview'
weight: 20

menu:
  main:
    identifier: 'architecture-overview'
    parent: 'technical-guide'
    Pre: 'Get an overview over the software architecture of Cawemo.'
---

Cawemo consists of two components: Cawemo and Camunda Account.
The latter is our solution for Identity and Access Management (IAM).
It enables single sign-on and central user management for Camunda products.
Camunda Account is initially bundled with Cawemo, but it is a separate application.
Cawemo and Camunda Account may be updated separately in the future when more Camunda products integrate Camunda Account.

To give you an overview, the following illustration shows the components of Cawemo and how they are interacting with each other:

{{<img src="../architecture.png">}}
