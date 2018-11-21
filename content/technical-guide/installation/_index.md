---
title: 'Installation'
weight: 10
layout: 'single'

menu:
  main:
    identifier: 'installation'
    parent: 'technical-guide'
---

## Introduction

This installation guide is targeting system administrators who want to install Cawemo on their IT infrastructure / on-premise. This version of Cawemo is exclusively available for Camunda Enterprise customers and requires a separately sold license. Note that Camunda also offers a [cloud-based SaaS version of Cawemo](http://www.cawemo.com) which is not the subject of these docs.

## Prerequisites

Cawemo consists of several components that are tied together with Docker Compose. In addition to those components that ship with Cawemo, a few external systems are required for running it, which need to be set up separately.

- Docker for Linux v17.03 or newer
- Docker Compose v1.23.0 or newer
- PostgreSQL Server v9.6 (newer versions _may_ work as well)
  - used as presistent storage for all Cawemo data (e.g. BPMN workflows, comments etc.)
- Camunda BPM engine v7.9+ with REST API enabled
  - Cawemo connects to the Camunda BPM REST API to authenticate users and validate user authorizations. All operations are read-only.

## 1. Log-in to Camunda Docker Registry

The Cawemo Docker images are hosted on our dedicated Docker registry and are available to enterprise customers only. You can browse the available images in our [Docker registry](https://repository.camunda.cloud/#browse/search/docker) after logging-in with your credentials.

Make sure to log-in correctly:

```
$ docker login registry.camunda.cloud
Username: your_username
Password: ******
Login Succeeded
```

## 2. Create docker-compose.yml file

Create a docker-compose.yml file in your server directory with the following content (::TODO::):

```
version: "3"
services:

  redis:
    image: redis:alpine
    ports:
      - "6379"
    networks:
      - frontend
    deploy:
      replicas: 2
      update_config:
        parallelism: 2
        delay: 10s
      restart_policy:
        condition: on-failure

  db:
    image: postgres:9.4
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backend
    deploy:
      placement:
        constraints: [node.role == manager]
```

## 3. Create a .env file

In the same server directory, create a .env file with the following content and adjust the values according to your own setup:

```
# Cawemo
CAWEMO_SERVER_HOST=my-host.com
CAWEMO_SERVER_URL=https://cawemo.my-host.com

# PostgreSQL Database
CAWEMO_DB_HOST=postgresql.my-host.com
CAWEMO_DB_PORT=5432
CAWEMO_DB_USER=cawemo
CAWEMO_DB_PASSWORD=top-secret
CAWEMO_DB_NAME=cawemo

# Camunda BPM
CAWEMO_CAMUNDA_ENGINE=camundaBPM.my-host.com/engine-rest
```

## 4. Configure your network

The Cawemo frontend (web-browser) needs to be able to connect to the Cawemo backend. Therefore make sure that

- the domain you have set up above as CAWEMO_SERVER_URL is reachable from within your network on port 8080
- websockets are supported

You might also want to consider setting up a proxy server (i.e. nginx) in front of the Cawemo server, which will allow you to configure SSL encryption etc.

## 5. Run Cawemo

You should now be able to start up Cawemo by issuing

```
docker-compose up
```

## 6. Usage

Point your web-browser to the URL you defined above as CAWEMO_SERVER_URL to verify that the login screen comes up.

You should now be able to log in with credentials of users set up in the Camunda BPM platform. For details on how to configure user access, consult the [user access management]({{< ref "/technical-guide/user-management/_index.md" >}}) section.
