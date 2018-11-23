---
title: 'User Access Management'
weight: 20

menu:
  main:
    identifier: 'user-management'
    parent: 'technical-guide'
---

Cawemo users are not managed within Cawemo itself, but rather in the Camunda BPM platform. For users to gain access to Cawemo, they need to be authorized, which can be achieved on different levels with different options. To learn more about how authorization in Camunda works, please consult the [authorization service documentation](https://docs.camunda.org/manual/latest/user-guide/process-engine/authorization-service/).

In order to be able to access Cawemo, a user needs to be granted access on resource type "application" with resource ID `cawemo` (or "\*" if you want to grant access for all applications including Cawemo). The permission needs to be set either to `ALL` or `ACCESS`. Both are treated equally, so there is no difference between them for now.

Authorizing users for Cawemo using the Camunda Admin application can be achieved in several ways:

{{< img src="Admin-GrantAccessAuthorizations.png" title="Grant Cawemo Access in Admin" >}}

1. The first option allows acces for Cawemo on a global level. With this setting all users are allowed to log-in to Cawemo.
2. The second option defines the access for a single user. The user `catalina` can now log-in to Cawemo.
3. The third option provides access on group level. All users belonging to the group `cawemo-users` can log-in to Cawemo.

It is also possible to revoke the Cawemo authorization for specific users or groups. For instance, you can define Cawemo on a global scale, but exclude the `engineers` group:

{{< img src="Admin-RevokeGroupAccess.png" title="Revoke Cawemo Access for group 'engineers' in Admin" >}}
