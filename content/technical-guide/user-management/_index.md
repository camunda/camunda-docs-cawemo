---
title: 'User Access Management'
weight: 50

menu:
  main:
    identifier: 'user-management'
    parent: 'technical-guide'
---

You can use the credentials from the Camunda Platform users to access Cawemo. However, for the users to gain access to Cawemo, they need to be authorized. This is not done in Cawemo itself, but needs to be configured in the Camunda Platform and can be achieved on different levels with different options. If you do not know how authorization in Camunda works, please have a look at the [authorization service documentation](https://docs.camunda.org/manual/latest/user-guide/process-engine/authorization-service/).

When defining an authorization to grant Cawemo access, the most important aspect is that you grant access on resouce type application with resource id "cawemo" ( or "\*" if you want to grant the access for all applications including Cawemo). The permissions you can set, are either choose `ALL` or `ACCESS`. They are treated equally, so there is no difference between them for now.

Authorizing users in admin could be done like in the following:

{{< img src="Admin-GrantAccessAuthorizations.png" title="Grant Cawemo Access in Admin" >}}

1. The first option allows acces for Cawemo on a global level. With this setting all users are allowed to log in into Cawemo.
2. The second option defines the access for a single user. The user `Kermit` can now log into Cawemo.
3. The third option provides access on group level. All users belonging to the group `cawemo-users` can log in into Cawemo.

It is also possible to revoke the Cawemo authorization for specific users or groups. For instance, you can define Cawemo on a global scale, but exclude the `engineers` group:

{{< img src="Admin-RevokeGroupAccess.png" title="Revoke Cawemo Access for group 'engineers' in Admin" >}}
