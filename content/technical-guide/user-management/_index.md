---

title: "User Access Management"
weight: 50

menu:
  main:
    identifier: "user-management"
    parent: "technical-guide"

---

{{< note title="Good to know!" class="info" >}}

Providing Optimize access to a user just enables him/her to log in to Optimize. To be able
to create reports the user also needs to have permission to access the engine data. To see
how this can be done please refer to the [Authorization Management]({{< ref "/technical-guide/authorization/_index.md" >}}) section.

{{< /note >}}

You can use the credentials from the Camunda Platform users to access Optimize. However, for the users to gain access to Optimize, they need to be authorized. This is not done in Optimize itself, but needs to be configured in the Camunda Platform and can be achieved on different levels with different options. If you do not know how authorization in Camunda works, please have a look at the [authorization service documentation](https://docs.camunda.org/manual/latest/user-guide/process-engine/authorization-service/).

When defining an authorization to grant Optimize access, the most important aspect is that you grant access on resouce type application with resource id "optimize" ( or "*" if you want to grant the access for all applications including Optimize). The permissions you can set, are either choose `ALL` or `ACCESS`. They are treated equally, so there is no difference between them for now. 

Authorizing users in admin could be done like in the following:

{{< img src="Admin-GrantAccessAuthorizations.png" title="Grant Optimize Access in Admin" >}}

1. The first option allows acces for Optimize on a global level. With this setting all users are allowed to log in into Camunda Optimize.
2. The second option defines the access for a single user. The user `Kermit` can now log into Camunda Optimize.
3. The third option provides access on group level. All users belonging to the group `optimize-users` can log in into Camunda Optimize.



It is also possible to revoke the Optimize authorization for specific users or groups. For instance, you can define Optimize on a global scale, but exclude the `engineers` group:

{{< img src="Admin-RevokeGroupAccess.png" title="Revoke Optimize Access for group 'engineers' in Admin" >}}



