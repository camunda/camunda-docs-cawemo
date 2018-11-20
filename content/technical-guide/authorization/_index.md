---

title: "Authorization Management"
weight: 50

menu:
  main:
    identifier: "authorization-management"
    parent: "technical-guide"

---

Defining authorizations for users is done based on process definition. To be more precise, you can specify which user has access to certain process definition including data related to that process definition. By that we mean the user can only see, create, edit and delete reports to process definitions he is authorized to.

The creation of an authorization is not done in Optimize itself, but needs to be configured in the Camunda Platform and can be achieved on different levels with different options. If you do not know how authorization in Camunda works, please have a look at the [authorization service documentation](https://docs.camunda.org/manual/latest/user-guide/process-engine/authorization-service/). That has the advantage that you don't need to define the authorizations several times.

When defining an authorization to grant or deny access to certain process definitions, the most important aspect is that you grant access on resource type process definition. You can then relate to a specific process definition by providing the definition key as resource id or use "*" as resource id if you want to grant the access to all definitions. To grant access to a definition, you need to set either `ALL` or `READ_HISTORY` as permission. Both permission settings are treated equally in Optimize, so there is no difference between them for now.

As an example, have a look how adding authorizations for process definitions could be done in Camunda Admin:

{{< img src="Admin-GrantDefinitionAuthorizations.png" title="Grant Optimize Access in Admin" >}}

1. The first option grants global read access for the process definition `invoice`. With this setting all users are allowed to see, update, create and delete reports related to the process definition `invoice` in Optimize.
2. The second option defines an authorization for a single user. The user `Kermit` can now see, update, create and delete reports related to the process definition `invoice` in Optimize.
3. The third option provides access on group level. All users belonging to the group `optimize-users` can see, update, create and delete reports related to the process definition `invoice` in Optimize.

It is also possible to revoke the process definition authorization for specific users or groups. For instance, you can define access for all process definitions on a global scale, but exclude the `engineers` group from access reports related to the `invoice` process:

{{< img src="Admin-RevokeDefinitionAuthorization.png" title="Revoke Optimize Access for group 'engineers' in Admin" >}}
