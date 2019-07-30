---
title: 'Migration & Upgrade'
weight: 30

menu:
  main:
    identifier: 'update'
    parent: 'technical-guide'
---

Roughly every quarter of a year a new minor version of Cawemo is released. This document guides you through the process of migrating from one Cawemo version to the next.

# Migration Steps

1.  Stop Cawemo
2.  Make a DB backup
3.  Update your `docker-compose.yml` file to the desired version
4.  Start Cawemo again
