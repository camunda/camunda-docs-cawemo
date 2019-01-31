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

This installation guide is targeting system administrators who want to install Cawemo on their IT infrastructure / on-premise. This version of Cawemo is exclusively available for Camunda Enterprise customers and requires a separately sold license. Note that Camunda also offers a [cloud-based SaaS version of Cawemo](https://cawemo.com/) which is not the subject of these docs.

## Prerequisites

Cawemo consists of several components that are tied together with [Docker Compose](https://docs.docker.com/compose/). In addition to those components that ship with Cawemo, a few external systems are required for running it, which need to be set up separately.

- Server with Linux operating system on `amd64` architecture
- [Docker CE](https://docs.docker.com/install/) 17.03 or newer
- [Docker Compose](https://docs.docker.com/compose/) 1.23.0 or newer
- [PostgreSQL](https://www.postgresql.org/) 9.6 (newer versions _may_ work as well)
  - used as presistent storage for all Cawemo data (e.g. BPMN workflows, comments etc.)
- [Camunda BPM](https://camunda.com/) 7.9 or newer with REST API enabled
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

## 2. Download `docker-compose.yml` file

Download this [docker-compose.yml]({{< refstatic "docker-compose.yml" >}}) file to your server directory.

## 3. Create a `.env` file

In the same server directory, create a `.env` file with the following content and adjust the values according to your own setup, especially the path to the license file.

{{< note title="Generating unique secrets" class="info" >}}
The below configuration lacks values for `SERVER_SESSION_COOKIE_SECRET` and `WEBSOCKET_SECRET` that each customer has to generate once before the first run. A long sequence of at least 32 random characters should be fine.

We do not ship with any default values to ensure that customers use unique secrets for security reasons.
{{< /note >}}

```
##########
# CAWEMO #
##########
SERVER_URL=https://cawemo.your-company.com
SERVER_HOST=cawemo.your-company.com
SERVER_HTTPS_ONLY=true
SERVER_SESSION_COOKIE_SECRET=

###############
# CAMUNDA BPM #
###############
CAMUNDABPM_URL=http://camundabpm.your-company.com/engine-rest
CAMUNDABPM_AUTH_ENABLED=false
CAMUNDABPM_AUTH_USER=http_user
CAMUNDABPM_AUTH_PASSWORD=http_pass

############
# DATABASE #
############
DB_HOST=postgresql.your-company.com
DB_PORT=5432
DB_NAME=cawemo
DB_USER=cawemo
DB_PASSWORD=top-secret-123

#########
# EMAIL #
#########
SMTP_HOST=mail.your-company.com
SMTP_PORT=587
SMTP_USER=cawemo
SMTP_PASSWORD=top-secret-123
SMTP_ENABLE_TLS=true
SMTP_FROM_ADDRESS=cawemo@your-company.com
SMTP_FROM_NAME=Cawemo

##############
# WEBSOCKETS #
##############
BROWSER_WEBSOCKET_HOST=cawemo.your-company.com
BROWSER_WEBSOCKET_PORT=8060
BROWSER_WEBSOCKET_FORCETLS=true
WEBSOCKET_SECRET=

################################
# FRONTEND STYLE CUSTOMIZATION #
################################
THEME_COLOR_PRIMARY=#2875cc
THEME_COLOR_SECONDARY=#00bfa5
THEME_COLOR_ACCENT=#343434
# A PNG file of 134px width and 20px height is recommended
THEME_LOGO_URL=/img/cawemo-enterprise-default.min.svg

###########
# LICENSE #
###########
LICENSE_FILE_PATH=/path/to/license.txt
```

## 4. Configure your network

To let users access Cawemo via their web-browsers there are a couple of requirements that the system administrator has to fulfill usually using some kind of reverse proxy server.

The `SERVER_URL` specified in the `.env` file must be accessible by the user's web-browser using depending on the setting of `SERVER_HTTPS_ONLY` via HTTPS with certificate validation or (not recommended) via insecure HTTP. This traffic has to be proxied to port `8080` on the host running the Cawemo Docker images.

In addition to that the reverse proxy must support websockets and allow the user's web-browser to connect to the `BROWSER_WEBSOCKET_HOST` and `BROWSER_WEBSOCKET_PORT` depending on the setting of `BROWSER_WEBSOCKET_FORCETLS` with TLS and certificate validation enabled or (not recommended) without TLS. This traffic has to be proxied to port `8060` on the host running the Cawemo Docker images.

Besides that make sure that Cawemo can correctly access other services like the PostgreSQL database, SMTP server, Camunda BPM instance, etc.

## 5. Run Cawemo

You should now be able to start up Cawemo by issuing:

```
docker-compose up
```

## 6. Validate installation

Point your web-browser to the URL you defined above as `SERVER_URL` to verify that the login screen comes up.

You should now be able to log in with credentials of users set up in the Camunda BPM platform. For details on how to configure user access, consult the [user access management]({{< ref "/technical-guide/user-management/_index.md" >}}) section.
