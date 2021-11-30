---
title: 'Configuration'
weight: 20

menu:
  main:
    identifier: 'technical-guide-configuration'
    parent: 'installation'
---

This page offers an overview of all the environment variables you'll need to specify in the `.env` configuration file.

# Cawemo

<table class="table table-striped">
  <tr>
    <th>Environment Variable</th>
    <th>Example Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>SERVER_URL</td>
    <td>https://cawemo.example.com</td>
    <td>
      URL at which users will access Cawemo. Please use the <b>domain root</b>.<br/>
      Internally, the traffic has to be proxied to the <i>cawemo-webapp</i> container (port 8080).
    </td>
  </tr>
  <tr>
    <td>SERVER_HOST</td>
    <td>cawemo.example.com</td>
    <td>Host part of SERVER_URL</td>
  </tr>
  <tr>
    <td>SERVER_HTTP_COMPRESSION_<wbr/>ENABLED</td>
    <td>true</td>
    <td>
      Enable HTTP response compression.
      By default, responses must be at least 2048 bytes in length for compression to be performed.
      You can configure this behavior by setting the <i>SERVER_HTTP_COMPRESSION_<wbr/>MIN_<wbr/>RESPONSE_<wbr/>SIZE_<wbr/>BYTES</i> property.<br/>
      <b>Set this to <i>false</i> if Cawemo is running behind a component that already compresses responses.</b>
    </td>
  </tr>
  <tr>
    <td>SERVER_HTTP_COMPRESSION_<wbr/>MIN_<wbr/>RESPONSE_<wbr/>SIZE_BYTES</td>
    <td>2048</td>
    <td>Minimum size of HTTP responses in bytes for compression to take effect.</td>
  </tr>
  <tr>
    <td>SERVER_HTTPS_ONLY</td>
    <td>true</td>
    <td>Enforce the usage of HTTPS when users access Cawemo in the browser</td>
  </tr>
  <tr>
    <td>SERVER_SESSION_COOKIE_SECRET</td>
    <td>****</td>
    <td>
      A unique secret of at least 32 characters used to sign Cawemo session cookies.<br/>
      <b>If left blank, a random value will be generated automatically by the startup script.</b>
    </td>
  </tr>
  <tr>
    <td>DB_HOST</td>
    <td>postgres.example.com</td>
    <td>Host name of the PostgreSQL instance</td>
  </tr>
  <tr>
    <td>DB_PORT</td>
    <td>5432</td>
    <td>Database port</td>
  </tr>
  <tr>
    <td>DB_NAME</td>
    <td>cawemo</td>
    <td>Database name for Cawemo. Please use <b>separate databases</b> for Cawemo and Camunda Account.</td>
  </tr>
  <tr>
    <td>DB_USER</td>
    <td>cawemo</td>
    <td>Database user</td>
  </tr> 
  <tr>
    <td>DB_PASSWORD</td>
    <td>****</td>
    <td>Database password</td>
  </tr>
  <tr>
    <td>SMTP_HOST</td>
    <td>mail.example.com</td>
    <td>Host name of the SMTP server used by both Cawemo and Camunda Account</td>
  </tr>
  <tr>
    <td>SMTP_PORT</td>
    <td>587</td>
    <td>SMTP server port</td>
  </tr>
  <tr>
    <td>SMTP_USER</td>
    <td>user</td>
    <td>SMTP user</td>
  </tr>
  <tr>
    <td>SMTP_PASSWORD</td>
    <td>****</td>
    <td>SMTP password</td>
  </tr>
  <tr>
    <td>SMTP_ENABLE_TLS</td>
    <td>true</td>
    <td>Enable or disable TLS encryption for SMTP connections</td>
  </tr>
  <tr>
    <td>SMTP_FROM_ADDRESS</td>
    <td>cawemo@example.com</td>
    <td>E-mail address that will be displayed as the sender of e-mails sent by Cawemo and Camunda Account</td>
  </tr>
  <tr>
    <td>SMTP_FROM_NAME</td>
    <td>Cawemo</td>
    <td>Name that will be displayed as the sender of e-mails sent by Cawemo and Camunda Account</td>
  </tr>
  <tr>
    <td>BROWSER_WEBSOCKET_HOST</td>
    <td>ws.example.com</td>
    <td>
      Name of the host on which the browser will access the Cawemo WebSockets server.<br/>
      Internally, the traffic has to be proxied to the <i>cawemo-websockets</i> container (port 8060).
    </td>
  </tr>
  <tr>
    <td>BROWSER_WEBSOCKET_PORT</td>
    <td>443</td>
    <td>Port number on which the browser will access the Cawemo WebSockets server</td>
  </tr>
  <tr>
    <td>BROWSER_WEBSOCKET_FORCETLS</td>
    <td>true</td>
    <td>Enable or disable TLS encryption for WebSocket connections initiated by the browser</td>
  </tr>
  <tr>
    <td>WEBSOCKET_SECRET</td>
    <td>****</td>
    <td>
      A unique secret of at least 32 characters used by Cawemo's <i>webapp</i> and <i>restapi</i> modules to
      authenticate to the WebSockets server.<br/>
      <b>If left blank, a random value will be generated automatically by the startup script.</b>
    </td>
  </tr>
  <tr>
    <td>THEME_COLOR_PRIMARY</td>
    <td>#2875cc</td>
    <td>HTML color code used for buttons and hyperlinks in e-mails sent by Cawemo</td>
  </tr>
  <tr>
    <td>HOST_LICENSE_FILE_PATH</td>
    <td>./../configuration/license-key.txt</td>
    <td>Path to the license key file</td>
  </tr>
</table>

# Camunda Account

<table class="table table-striped">
  <tr>
    <th>Environment Variable</th>
    <th>Example Value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>IAM_BASE_URL</td>
    <td>https://iam.example.com</td>
    <td>
      URL at which users will access Camunda Account. Please note that it must be different from Cawemo's SERVER_URL.<br/>
      Internally, the traffic has to be proxied to the <i>iam-router</i> container (port 8090).
    </td>
  </tr>
  <tr>
    <td>IAM_TOKEN_SIGNING_KEY</td>
    <td>****</td>
    <td>
      A 4096 bits RSA private key in JSON Web Key (JWK) format. It will be used to sign the access tokens issued by Camunda Account.<br/>
      <b>If left blank, a JWK will be generated automatically by the startup script.</b><sup><a href="#notes">1)</a></sup><br/>
    </td>
  </tr>
  <tr>
    <td>CLIENT_SECRET</td>
    <td>****</td>
    <td>
      A unique secret of at least 32 characters used by Cawemo to authenticate to Camunda Account.<br/>
      <b>If left blank, a random value will be generated automatically by the startup script.</b>
    </td>
  </tr>
  <tr>
    <td>IAM_DB_HOST</td>
    <td>postgres.example.com</td>
    <td>Host name of the PostgreSQL instance</td>
  </tr>
  <tr>
    <td>IAM_DB_PORT</td>
    <td>5432</td>
    <td>Database port</td>
  </tr>
  <tr>
    <td>IAM_DB_NAME</td>
    <td>iam</td>
    <td>Database name for Camunda Account. Please use <b>separate databases</b> for Cawemo and Camunda Account.</td>
  </tr>
  <tr>
    <td>IAM_DB_USER</td>
    <td>iam</td>
    <td>Database user</td>
  </tr> 
  <tr>
    <td>IAM_DB_PASSWORD</td>
    <td>****</td>
    <td>Database password</td>
  </tr>
  <tr>
    <td>IAM_DATABASE_ENCRYPTION_KEY</td>
    <td>****</td>
    <td>
      A unique secret of 32 characters used to encrypt client secrets in the Camunda Account database.<br/>
      <b>If left blank, a random value will be generated automatically by the startup script.</b>
  </tr>
  <tr>
    <td>LDAP_ENABLED</td>
    <td>false</td>
    <td>Enable or disable LDAP integration<sup><a href="#notes">2)</a></sup></td>
  </tr>
</table>

### Notes
<sup>1)</sup> If you'd like to generate the JWK yourself, please use the following command:
```
docker run --rm -t \
  registry.camunda.cloud/iam-ee/iam-utility:v1.1.6 \
  yarn run generate-jwk
```

<sup>2)</sup> Please refer to the [LDAP configuration options]({{< ref "ldap-support.md#configuration-options">}}) for the
additional environment variables that will be required if you enable the LDAP integration.
