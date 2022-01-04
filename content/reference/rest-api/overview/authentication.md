---
title: 'Authentication'
weight: 10

menu:
  main:
    identifier: 'rest-api-authentication'
    parent: 'rest-api-overview'
---

{{< note title="Heads Up!" class="warning" >}}
Accessing Cawemo's public API requires a valid Enterprise license.
{{< /note >}}

Every request to Cawemo's public API requires the use of HTTP Basic Authentication.
Your request to Cawemo's public API will be successful only if you pass a valid user id and API key combination in the authorization header.
The user id and API key combination can be retrieved from the settings page of your organization:

{{<img src="../../../../technical-guide/integrations/api-keys.png">}}

To learn more about best practices regarding API keys please visit our [user guide]({{< ref "/user-guide/settings.md#managing-api-keys-enterprise-only" >}}).

Make sure you always Base64-encode your credentials before adding them to the `Authentication: Basic` HTTP header.

In the following cURL request example, you would replace \<user_id> and \<api_key> with your credentials before sending the request:

```
curl -v -u <user_id>:<api_key> "https://cawemo.com/api/v1/catalogs"
```
