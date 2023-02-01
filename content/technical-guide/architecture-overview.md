---
title: 'Architecture Overview'
weight: 20

menu:
  main:
    identifier: 'architecture-overview'
    parent: 'technical-guide'
    Pre: 'Get an overview over the software architecture of Cawemo Enterprise Edition.'
---

Cawemo Enterprise Edition consists of two components: Cawemo and Camunda Account.
The latter is our solution for Identity and Access Management (IAM).
It enables single sign-on and central user management for Cawemo.
Camunda Account is initially bundled with Cawemo, but it is a separate application.

To give you an overview, the following illustration shows the components of Cawemo EE and how they are interacting with each other:

{{<img src="../architecture.png">}}
