---
title: 'Reverse Proxy Configuration'
weight: 60

menu:
  main:
    identifier: 'reverse-proxy-configuration'
    parent: 'installation'
---

The Cawemo distribution includes a sample configuration for running Cawemo behind an [automated NGINX reverse proxy for Docker with SSL support](https://github.com/nginx-proxy/nginx-proxy).

To use the reverse proxy in your production environment, please follow the steps below (assuming that you have
already downloaded and configured Cawemo according to the general [installation guide]({{< ref "_index.md">}})).

# 1. Extend the `.env` File

Add the following environment variables to the `.env.production` file and adjust the values according to your own setup.

<table class="table table-striped">
  <tr>
    <th>Environment Variable</th>
    <th>Example Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>IAM_SERVER_HOST</td>
    <td>iam.example.com</td>
    <td>Host part of IAM_BASE_URL</td>
  </tr>
  <tr>
    <td>SERVER_TLS_CERTIFICATES_PATH</td>
    <td>/path/to/certificates</td>
    <td>Path of the server directory containing your SSL certificates</td>
  </tr>
</table>

# 2. Provide SSL Certificates

You have to provide SSL certificates for the following host names:

* `SERVER_HOST`
* `BROWSER_WEBSOCKET_HOST`
* `IAM_SERVER_HOST`

The certificates and their corresponding private keys must be stored in the [PEM file format](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail)
and must all be placed in the directory configured in `SERVER_TLS_CERTIFICATES_PATH`.

The files should be named after a certain scheme:

* Individual certificates should be named after the host name with a _.crt_ and _.key_ extension.
  For example, a value of `SERVER_HOST=cawemo.example.com` should have a `cawemo.example.com.crt` and `cawemo.example.com.key` file in the certificate directory.
* Wildcard certificates should be named after the domain name with a _.crt_ and _.key_ extension.
  For example, a value of `SERVER_HOST=cawemo.example.com` needs `example.com.crt` and `example.com.key` files in the certificate directory.

For more detailed information on the reverse proxy's SSL configuration options please refer to the [official documentation](https://github.com/nginx-proxy/nginx-proxy#ssl-support).

# 3. Run Cawemo

To run Cawemo with the provided reverse proxy, execute the startup script with the additional argument `--reverse-proxy`:
```
./start-cawemo.sh --production --reverse-proxy
```
Point your web browser to the URL you specified in `SERVER_URL` to verify that the application is running.
