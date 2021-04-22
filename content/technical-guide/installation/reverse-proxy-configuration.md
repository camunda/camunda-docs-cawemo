---
title: 'Reverse Proxy Configuration'
weight: 70

menu:
  main:
    identifier: 'reverse-proxy-configuration'
    parent: 'installation'
---

This page offers a sample configuration of how to run Cawemo with a pre-configured reverse proxy server with SSL support using NGINX.
To do so, please follow the following steps:

## 1. Download `docker-compose.reverse-proxy.yml`

Download this [docker-compose.reverse-proxy.yml]({{< refstatic "docker-compose.reverse-proxy.yml" >}}) file to the same location you put the `docker-compose.yml` [from step 2 of the on-premise installation]({{< ref "_index.md#2-download-docker-composeyml-file">}}).

## 2. Extend the `.env` File

Add these values to the `.env` file you created [in step 3 of the on-premise installation]({{< ref "_index.md#3-create-an-env-file">}}) and adjust the values according to your own setup.

```
IAM_SERVER_HOST=iam.example.com
SERVER_TLS_CERTIFICATES_PATH=/path/to/certificates
```

## 3. Create a Folder For Your Certificates

You have to provide SSL certificates for the host names used in `SERVER_HOST`, `BROWSER_WEBSOCKET_HOST` and `IAM_SERVER_HOST` via the path configured in `SERVER_TLS_CERTIFICATES_PATH`.
The certificates must be named after a certain scheme:

* For individual certificates use _my.domain.tld.{key,crt,pem}_.
* For certificate bundles use anything other than the above, e.g. _domain.tld.{crt,key,pem}_.

Beware that self-signed certificates won't work.

## 4. Run Cawemo

Use the following command for running Cawemo with the provided reverse proxy:

```
docker-compose -f docker-compose.yml -f docker-compose.reverse-proxy.yml up -d
```

Point your web browser to the URL you defined above as `SERVER_URL` to verify that the application is running.
