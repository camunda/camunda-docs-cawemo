---
title: 'On-Premise Installation'
weight: 10
layout: 'single'

menu:
  main:
    identifier: 'installation'
    parent: 'technical-guide'
    Pre: 'Read in this section how you install Cawemo Enterprise On-Premise.'
---

## Introduction

This installation guide is targeting system administrators who want to install Cawemo Enterprise On-Premise **1.4** on their own IT infrastructure or private cloud. This version of Cawemo is exclusively available for Camunda Enterprise customers and requires a separately sold license.

## Prerequisites

Cawemo consists of several components that are tied together with [Docker Compose](https://docs.docker.com/compose/). In addition to those components that ship with Cawemo, a few external systems are required for running it, which need to be set up separately.

- Server with Linux operating system on `amd64` architecture
- [Docker CE](https://docs.docker.com/install/) 17.03 or newer
- [Docker Compose](https://docs.docker.com/compose/) 1.23.0 or newer
- [PostgreSQL](https://www.postgresql.org/) 9.6 (newer versions _may_ work as well)
  - used as presistent storage for all Cawemo data (e.g. BPMN workflows, comments etc.)

**TODO** make sure to tell the customers (this is not really the right spot ...)
* what IAM is and why IAM is added to Cawemo
* that IAM will in a later release be separated (so they might want to choose a separate database for IAM, the components that are going to be a separate IAM installation can be seen from the docker-compose.iam.yml file. this is relevant information for the 2 customers who craft Kubernetes or OpenShift manifests from the compose files)


## 1. Log-in to Camunda Docker Registry

The Cawemo Docker images are hosted on our dedicated Docker registry and are available to enterprise customers only. You can browse the available images in our [Docker registry](https://registry.camunda.cloud) after logging-in with your credentials.

Make sure to log-in correctly:

```
$ docker login registry.camunda.cloud
Username: your_username
Password: ******
Login Succeeded
```

## 2. Download `docker-compose.yml` files

Download the [docker-compose.iam.yml]({{< refstatic "docker-compose.iam.yml" >}})
and [docker-compose.cawemo.yml]({{< refstatic "docker-compose.cawemo.yml" >}}) files to your server directory.

## 3. Create `.env` files

**TODO** Include/paste the [.env.iam]({{< refstatic ".env.iam" >}}) to be customized by the customer's admin

In the same server directory, create a `.env.cawemo` file with the following content and adjust the values according to your own setup, especially the path to the license file.

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
HOST_LICENSE_FILE_PATH=/path/to/license.txt
```

## 4. Configure your network

**TODO** Adapt to IAM - will also wait for incoming connections at 8080

To let users access Cawemo via their web-browsers there are a couple of requirements that the system administrator has to fulfill usually using some kind of reverse proxy server.

The `SERVER_URL` specified in the `.env` file must be accessible by the user's web-browser using depending on the setting of `SERVER_HTTPS_ONLY` via HTTPS with certificate validation or (not recommended) via insecure HTTP. This traffic has to be proxied to port `8080` on the host running the Cawemo Docker images.

In addition to that the reverse proxy must support websockets and allow the user's web-browser to connect to the `BROWSER_WEBSOCKET_HOST` and `BROWSER_WEBSOCKET_PORT` depending on the setting of `BROWSER_WEBSOCKET_FORCETLS` with TLS and certificate validation enabled or (not recommended) without TLS. This traffic has to be proxied to port `8060` on the host running the Cawemo Docker images.

Besides that make sure that Cawemo can correctly access other services like the PostgreSQL database, SMTP server etc.

## 5. Run Cawemo

You should now be able to start up Cawemo by issuing:

```
cat .env.iam .env.cawemo > .env \
&& docker-compose --env-file .env -f docker-compose.iam.yml -f docker-compose.cawemo.yml up
```

Point your web-browser to the URL you defined above as `SERVER_URL` to verify that the application is running.

## 6. Configure Admin user

For the initial setup of Cawemo and to add more users, please setup an Admin user by accessing the following URL: [`SERVER_URL/signup?token=16510354-c1c5-40e0-813c-cfb55bac372a`](https://cawemo.your-company.com/signup?token=16510354-c1c5-40e0-813c-cfb55bac372a)

Once the Admin user has been created, you will be able to invite more users to Cawemo from the admin's User Menu -> Settings -> Manage Members overlay.

Make sure that your SMTP server is up and running such that the users will receive invitations via email.
