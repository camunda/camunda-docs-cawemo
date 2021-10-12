---
title: 'Installation on Windows'
weight: 70

menu:
  main:
    identifier: 'technical-guide-installation-on-windows'
    parent: 'installation'
---

Currently, running Cawemo on a Windows operating system still requires a few manual steps, since a dedicated startup
script for Windows is not yet available.

# Installation Steps
Please make sure you have followed the [Prerequisites]({{< ref "_index.md#prerequisites" >}}) section from the
installation guide before continuing. Also, this guide assumes that you're installing Cawemo on your local Windows
computer.

## Create Secrets
Please provide values for the following environment variables in the `configuration/.env.demo` file (please refer to the
[Configuration]({{< ref "configuration.md" >}}) page for a description of these settings):

* `SERVER_SESSION_COOKIE_SECRET`
* `WEBSOCKET_SECRET`
* `CLIENT_SECRET`
* `IAM_DATABASE_ENCRYPTION_KEY`

Each value should be a unique sequence of 32 random characters. 

## Create Token Signing Key
For `IAM_TOKEN_SIGNING_KEY`, please generate a JSON Web Key (JWK) using the RS256 algorithm. We provide a tool for
generating a 4096 bit JWK:
```
docker run --rm -t ^
  registry.camunda.cloud/iam-ee/iam-utility:v1.1.6 ^
  yarn run generate-jwk
```

## Run Cawemo With Docker Compose
In order to start Cawemo, please execute the following `docker-compose` command from the root of your Cawemo directory:
```
docker-compose ^
  -f docker-compose/docker-compose.yml ^
  -f docker-compose/docker-compose.demo.yml ^
  --env-file configuration/.env.demo ^
  up -d
```

# Known Limitations
Please note that the [Reverse Proxy Configuration]({{< ref "reverse-proxy-configuration.md" >}}) is generally not
supported on Windows, since it is using Unix sockets.
