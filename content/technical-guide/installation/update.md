---
title: 'Migration & Upgrade'
weight: 30

menu:
  main:
    identifier: 'update'
    parent: 'installation'
---

Roughly every quarter of a year a new minor version of Cawemo is released. This document guides you through the process of migrating from one Cawemo version to the next.

# Migrate Cawemo 1.4 -> 1.5

Cawemo 1.5 integrates a new identity and access management (IAM) component that requires users from Cawemo to be
migrated to IAM.

1.  Stop Cawemo
1.  Make a DB backup
1.  Update your [.env]({{< refstatic ".env" >}}) and [docker-compose.yml]({{< refstatic "docker-compose.yml" >}}) file
    by working through [installation instructions](TODO) (**TODO**: How to link these?) until including
    [Section 4: Configure your network](TODO) (**TODO**: How to link this, can the headline name be copied programmatically?)
1.  Start the IAM `backend` service e.g. with `docker-compose backend up -d`
    **TODO** Wait for startup ... (describe logs) / health check endpoint
1.  Migrate the Cawemo database to the IAM ([see below](#migrating-the-cawemo-database-to-iam)) (**TODO** is the link set correctly?)
1.  Start all other services e.g. using `docker-compose up -d`

## Migrating the Cawemo database to IAM

**TODO** Instructions are based on https://github.com/cawemo/cawemo-iam-user-migration . The docker image is not yet
available from the Docker registry: build it locally

The migration script will copy your Cawemo users to your local IAM database. Cawemo 1.5 will then use IAM to manage its
users.

Make sure you are logged in to the Camunda Docker registry (required only once):

```
$ docker login registry.camunda.cloud
Username: your_username
Password: ******
Login Succeeded
```

Run the Dockerized migration script with your updated `.env` file:

**TODO** Not sure whether the docker image is the final one, yet

```shell script
docker run --rm --env-file .env registry.camunda.cloud/team-cawemo/cawemo-iam-user-migration:master
```

# Other versions

1.  Stop Cawemo
1.  Make a DB backup
1.  Update your [docker-compose.yml]({{< refstatic "docker-compose.yml" >}}) file to the desired version **TODO** env also
1.  Start Cawemo again
