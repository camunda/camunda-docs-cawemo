---
title: 'Migration & Upgrade'
weight: 30

menu:
  main:
    identifier: 'update'
    parent: 'installation'
---

Roughly every quarter of a year a new minor version of Cawemo is released. This document guides you through the process of migrating from one Cawemo version to the next.

{{< note title="Updating from an older version of Cawemo?" class="warning" >}} If you are still using an older version of Cawemo
(version < 1.4) and want to upgrade to version 1.5, please follow
[the steps described at the end of this page](#migrate-from-an-older-version-to-15).{{< /note >}}

# Migrate from version 1.4 to 1.5

Cawemo 1.5 integrates Camunda Account, our new Identity and Access Management (IAM) component that requires users to be
migrated from Cawemo to Camunda Account. Cawemo 1.5 will then use Camunda Account to manage its users.
### Migration steps
1. Stop Cawemo
1. Make a database backup
1. Update your [.env]({{< refstatic ".env" >}}) and [docker-compose.yml]({{< refstatic "docker-compose.yml" >}}) file
   by working through steps **1 to 4** of the [installation instructions]({{< ref "_index.md" >}}). **Make sure that
   you do _not_ start Cawemo yet.**
1. Start the Camunda Account `backend` service _only_ with:
   ```
   docker-compose up -d backend
   ```
1. Make sure that the Camunda Account backend has started successfully by checking that
   ```
   docker-compose ps backend
   ```
   returns `Up (healthy)` in the `State` column. This is based on the health check and takes around 30 seconds. 
1. Migrate the users from the Cawemo database to Camunda Account [as described below](#migrate-user-data-from-cawemo-to-camunda-account).
1. Once the user migration has been finished, start all other services (see [step 5]({{< ref "_index.md#5-run-cawemo" >}})) with:
   ```
   docker-compose up -d
   ```

### Migrate user data from Cawemo to Camunda Account

We provide a migration script that will copy the existing Cawemo users to the Camunda Account database.

Make sure you are logged in to the Camunda Docker registry (required only once):

```
$ docker login registry.camunda.cloud
Username: your_username
Password: ******
Login Succeeded
```

Run the Dockerized migration script with your updated `.env` file:
```
docker run -it --rm --env-file .env \
  registry.camunda.cloud/cawemo-ee/cawemo-iam-user-migration:1.5.0
```
You should see the following output in the end, indicating a successful migration:
```
data migration completed successfully
```
# Migrate from an older version to 1.5
If you are still using an older version of Cawemo (< 1.4), you need to **migrate to version 1.4 first** before you can
[migrate to version 1.5](#migrate-from-version-14-to-15):

1. Stop Cawemo
1. Make a database backup
1. Update your [docker-compose.yml](https://docs.camunda.org/cawemo/1.4/docker-compose.yml) and `.env` file
   according to the [installation instructions for version 1.4.](https://docs.camunda.org/cawemo/1.4/technical-guide/installation)
1. Start Cawemo again
1. Proceed with the [steps listed above](#migrate-from-version-14-to-15)
