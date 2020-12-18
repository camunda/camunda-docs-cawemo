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

This installation guide is targeting system administrators who want to install Cawemo Enterprise On-Premise **1.5** on their own IT infrastructure or private cloud. This version of Cawemo is exclusively available for Camunda Enterprise customers and requires a separately sold license.

{{< note title="Heads Up!" class="warning" >}}If you upgrade an existing installation of Cawemo, please follow the [migration guide]({{< ref update.md >}}), as we have introduced Camunda's new Identity and Access Management solution (IAM) with this release.{{< /note >}}

Camunda Identity and Access Management enables single sign-on and central user management for Camunda products. Camunda IAM is initially bundled with
Cawemo, but it is a separate application. Cawemo and Camunda IAM may be updated separately when more Camunda products integrate Camunda IAM.

## Prerequisites

Cawemo consists of several components that are tied together with [Docker Compose](https://docs.docker.com/compose/). In addition to those components that ship with Cawemo, a few external systems are required for running it, which need to be set up separately.

- Server with Linux operating system on `amd64` architecture
- [Docker CE](https://docs.docker.com/install/) 17.03 or newer
- [Docker Compose](https://docs.docker.com/compose/) 1.23.0 or newer
- [PostgreSQL](https://www.postgresql.org/) 9.6 (newer versions _may_ work as well)
  - used as presistent storage for all Cawemo data (e.g. BPMN workflows, comments etc.)

## 1. Log-in to Camunda Docker Registry

The Cawemo Docker images are hosted on our dedicated Docker registry and are available to enterprise customers only. You can browse the available images in our [Docker registry](https://registry.camunda.cloud) after logging-in with your credentials.

Make sure to log-in correctly:

```
$ docker login registry.camunda.cloud
Username: your_username
Password: ******
Login Succeeded
```

## 2. Download `docker-compose.yml` file

Download this [docker-compose.yml]({{< refstatic "docker-compose.yml" >}}) file to your server directory.

## 3. Create an `.env` file

In the same server directory, create a `.env` file with the following content and adjust the values according to your own setup, especially the path to the license file.

{{< note title="Generating unique secrets" class="info" >}}
The below configuration lacks values for
* `SERVER_SESSION_COOKIE_SECRET`
* `WEBSOCKET_SECRET`
* `CLIENT_SECRET`
* `IAM_DATABASE_ENCRYPTION_KEY`
* `IAM_TOKEN_SIGNING_KEY`

that each customer has to generate once before the first run.
Unless otherwise noted, a long sequence of at least 32 random characters should be fine.

For `IAM_TOKEN_SIGNING_KEY`, please generate a JSON Web Key (JWK) using the `RS256` algorithm.
We provide a tool for generating a 4096 bit JWK:

```shell script
docker run --rm -t registry.camunda.cloud/iam-ee/iam-utility:v1.0.0 yarn run generate-jwk
```

We do not ship with any default values to ensure that customers use unique secrets for security reasons.
{{< /note >}}

```
{{< readFile "static/.env" >}}
```

## 4. Configure your network

To let users access Cawemo via their web-browsers there are a couple of requirements that the system administrator has to fulfill usually using some kind of reverse proxy server.

The `SERVER_URL` and `IAM_BASE_URL` specified in the `.env` file must be accessible by the user's web-browser via HTTPS with certificate validation.

* The traffic for Cawemo has to be proxied to port `8080` on the host running the Docker containers.
* The traffic for Camunda IAM has to be proxied to port `8090` on the host running the Docker containers.
* The domain configured for Camunda IAM must have a DNS resolution configured to be accessible to the web browser and the Cawemo backend (Docker container).
* In addition to that the reverse proxy must support websockets and allow the user's web-browser to connect to the `BROWSER_WEBSOCKET_HOST` and `BROWSER_WEBSOCKET_PORT` depending on the setting of `BROWSER_WEBSOCKET_FORCETLS` with TLS and certificate validation enabled. This traffic has to be proxied to port `8060` on the host running the Cawemo Docker containers.

Please also ensure that Cawemo and Camunda IAM can correctly access other services like the PostgreSQL database, SMTP server etc.

## 5. Run Cawemo

You should now be able to start up Cawemo by issuing:

```
docker-compose up -d
```

Point your web browser to the URL you defined above as `SERVER_URL` to verify that the application is running.

## 6. Configure admin user

For the initial setup of Cawemo and to add more users, you need to create an admin user. When you open Cawemo for the
first time, you will see an *Admin Setup* page. Please enter your e-mail address there and continue with the sign-up.

Once the admin user has been created, you will be able to invite more users to Cawemo. To do so, please open the *Settings*
page from the user menu and click on *Manage members*.

Make sure that your SMTP server is up and running so that the users will receive invitations via email.
