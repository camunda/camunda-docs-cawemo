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

# Introduction

This installation guide for Cawemo Enterprise On-Premise **1.9** is targeting:

* users who want to install Cawemo on their local computer for testing or demo purposes (see [Demo Setup](#demo-setup))
* system administrators who want to install Cawemo on their own IT infrastructure or private cloud for production use
  (see [Production Setup](#production-setup))

For both cases please make sure to go through the [Prerequisites]({{< ref "#prerequisites" >}}) section first.

{{< note title="Heads Up!" class="warning" >}}
If you upgrade an existing installation of Cawemo, please follow the [update & migration guide]({{< ref "update/_index.md" >}}).
{{< /note >}}

# Prerequisites

## Get an Enterprise License
This version of Cawemo is exclusively available for Camunda Enterprise customers and requires a separately sold license.
You can also sign up for a [free 30-day trial](https://camunda.com/download/enterprise) of the Camunda Enterprise Platform,
which includes Cawemo.

## Install Docker with Docker Compose
Cawemo consists of several components (see [Architecture Overview]({{< ref "architecture-overview.md" >}})) that are tied together with [Docker Compose](https://docs.docker.com/compose/).
Therefore, the following software needs to be installed:

- [Docker CE](https://docs.docker.com/install/) 19.03 or newer
- [Docker Compose](https://docs.docker.com/compose/) 1.25.0 or newer

## Log In to Camunda Docker Registry
The Cawemo Docker images are hosted on our dedicated Docker registry and are available to Enterprise customers only.
You need to log in to the registry once from the computer (or server) you will be running Cawemo on, so that the Docker
images can be pulled subsequently. Please use the credentials you received from Camunda to log in:

```
$ docker login registry.camunda.cloud
Username: your_username
Password: ******
Login Succeeded
```

## Download Cawemo
Download [cawemo-1.9.0.zip]({{< refstatic "download/cawemo-1.9.0.zip" >}}) or [cawemo-1.9.0.tar.gz]({{< refstatic "download/cawemo-1.9.0.tar.gz" >}})
and unzip the contents into a local directory on your computer or a directory on the server (depending on the use case).
Please refer to the included `README.txt` for a description of the different files included in the archive.

## Provide the License Key
Replace the contents of `configuration/license-key.txt` with the (trial) license key you received from Camunda.

# Demo Setup
## Supported Operating Systems
Currently, the easy demo setup (as described below) is only available on Linux and macOS. On Windows, a few manual
steps will be required to get Cawemo up and running. For more details please refer to
[Installation on Windows]({{< ref "installation-on-windows.md" >}}).

## Run Cawemo
We ship a ready-to-use configuration – which already includes a [PostgreSQL](https://www.postgresql.org/) database and
[MailHog](https://github.com/mailhog/MailHog) as SMTP server – that can be used to run Cawemo in a demo setup on your
local computer. No manual configuration changes or other external applications are required.

Just run the startup script without any arguments:
```
./start-cawemo.sh
```
The script will wait until all Docker containers have been successfully started. Once it has finished, point your web
browser to http://localhost:8080 to verify that the application is running.

# Production Setup

## Set Up the Infrastructure

In addition to the components that ship with Cawemo, a few external systems are required for running it, which need to be set up separately.

- Server with Linux operating system on `amd64` architecture
- [PostgreSQL](https://www.postgresql.org/) – supported versions: 10, 11, 12, 13 (newer versions _may_ work as well)
  - Postgres is used as persistent storage for all Cawemo data (e.g. BPMN workflows, comments etc.) as well as Camunda Account data.
  - Please set up two separate databases for Cawemo and Camunda Account.
  - Note: Cawemo's database user needs to be granted the `superuser` privilege.
- SMTP server
  - Both Cawemo and Camunda Account require an SMTP server to send e-mails to the users (e.g. when a new user is invited to join Cawemo).

## Update the Configuration File

Adjust the values in `configuration/.env.production` according to your own setup. Please refer to the
[Configuration]({{< ref "configuration.md" >}}) page for a description of the different settings.

If you'd like to enable the LDAP integration of Camunda Account, please refer to [LDAP Support]({{< ref "ldap-support.md" >}}).

## Configure Your Network
In order to enable users to access Cawemo via their web browsers, please configure your network infrastructure as
follows (e.g. by using some kind of reverse proxy server):

* The `SERVER_URL` and `IAM_BASE_URL` specified in the `.env.production` file must be accessible by web browsers via HTTPS with certificate validation.
  * The default configuration enforces the use of HTTPS.
    You can change this by setting `SERVER_HTTPS_ONLY=false`, but we do **not** recommend doing this in a production environment.
* The traffic for Cawemo (from `SERVER_URL`) has to be proxied to the `cawemo-webapp` container (port `8080`).
* The traffic for Camunda Account (from `IAM_BASE_URL`) has to be proxied to the `iam-router` container (port `8090`).
* The reverse proxy must support WebSockets and allow web browsers to connect to the `BROWSER_WEBSOCKET_HOST`
and `BROWSER_WEBSOCKET_PORT` with TLS and certificate validation enabled.
  * The default configuration enforces the use of TLS for WebSocket connections.
    You can change this by setting `BROWSER_WEBSOCKET_FORCETLS=false`, but we do **not** recommend doing this in a production environment.
* The WebSockets traffic (from `BROWSER_WEBSOCKET_HOST`) has to be proxied to the `cawemo-websockets` container (port `8060`).

Please also ensure that Cawemo and Camunda Account can correctly access the PostgreSQL database and the SMTP server.

For an example on how to configure Cawemo using a reverse proxy server with SSL support please refer to [Reverse Proxy Configuration]({{< ref "reverse-proxy-configuration.md" >}}).

## Run Cawemo
Run the startup script with the additional argument `--production`:
```
./start-cawemo.sh --production
```
The script will wait until all Docker containers have been successfully started. Once it has finished, point your web
browser to the URL you specified in `SERVER_URL` to verify that the application is running.

# Configure Admin User

## When LDAP Is Disabled

For the initial setup of Cawemo and to add more users, you need to create an admin user. When you open Cawemo for the
first time, you will see an *Admin Setup* page. Please enter your e-mail address there and continue with the sign-up.

Once the admin user has been created, you will be able to invite more users to Cawemo. To do so, please open the *Settings*
page from the user menu and click on *Manage members*.

Make sure that your SMTP server is up and running so that the users will receive invitations via email.

## When LDAP Is Enabled

The first user that logs into Cawemo with their LDAP credentials acts as admin user.
Subsequent users that log in are added as collaborators of the admin's organization.
