---
title: 'Reverse Proxy Configuration'
weight: 70

menu:
  main:
    identifier: 'reverse-proxy-configuration'
    parent: 'installation'
---

This page offers a sample configuration for running Cawemo with [an automated NGINX reverse proxy for Docker with SSL support](https://github.com/nginx-proxy/nginx-proxy).
To do so, please follow the following steps:

## 1. Download `docker-compose.reverse-proxy.yml`

Download this [docker-compose.reverse-proxy.yml]({{< refstatic "docker-compose.reverse-proxy.yml" >}}) file to the same location you put the `docker-compose.yml` [from step 2 of the on-premise installation]({{< ref "_index.md#2-download-docker-compose-yml-file">}}).

## 2. Extend the `.env` File

Add these values to the `.env` file you created [in step 3 of the on-premise installation]({{< ref "_index.md#3-create-an-env-file">}}) and adjust the values according to your own setup.

```
IAM_SERVER_HOST=iam.example.com
SERVER_TLS_CERTIFICATES_PATH=/path/to/certificates
```

## 3. Create a Folder For Your Certificates

You have to provide SSL certificates for the host names used in `SERVER_HOST`, `BROWSER_WEBSOCKET_HOST` and `IAM_SERVER_HOST` via the path configured in `SERVER_TLS_CERTIFICATES_PATH`.
The certificates and their corresponding private keys must be provided in the [PEM file format](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail).
They should be named after a certain scheme:

* Individual certificates should be named after the host name with a _.crt_ and _.key_ extension.
  For example, a value of `SERVER_HOST=foo.example.com` should have a `foo.example.com.crt` and `foo.example.com.key` file in the certificate directory.
* Wildcard certificates should be named after the domain name with a _.crt_ and _.key_ extension.
  For example, a value of `SERVER_HOST=foo.example.com` needs `example.com.crt` and `example.com.key` files in the certificate directory.

Beware that self-signed certificates won't work.
For more detailed information on the reverse proxy's SSL configuration options see the [official documentation](https://github.com/nginx-proxy/nginx-proxy#ssl-support).

## 4. Run Cawemo

Use the following command for running Cawemo with the provided reverse proxy:

```
docker-compose -f docker-compose.yml -f docker-compose.reverse-proxy.yml up -d
```

Point your web browser to the URL you defined above as `SERVER_URL` to verify that the application is running.
