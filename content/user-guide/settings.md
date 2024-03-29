---
title: 'Settings'
weight: 80

menu:
  main:
    identifier: 'settings'
    parent: 'user-guide'
    Pre: ""
---

This view offers various settings options.

## Notification Preferences

Whether a user wants to receive emails informing about new mentions in [comments](../diagrams#comments) can be adjusted per project.

## Managing API Keys

Users can create API Keys that are required to configure [Cawemo's Public API](../../reference/rest-api/) and the [Camunda Platform Engine](../../technical-guide/integrations/engine/) and [Camunda Modeler](../../technical-guide/integrations/modeler/) integrations.

For use cases located at an organizational level (i.e. Public API and Engine Integration) we recommend creating a separate Cawemo account that owns all API keys.

## Managing Members (Admin Only)

Admins can view all users and remove them from the organization individually.
Upon removal all projects the user was the only admin of are transferred to an admin and the user is deleted from the Cawemo database.

_Note:_ The deletion is not propagated to Camunda Account.
Users are still able to log in after they were removed from the organization.

### When LDAP Is Disabled

Admins can invite new users to sign up or resend invitations.

_Note:_ After users are deleted on the LDAP server the deletion is propagated neither to Camunda Account nor Cawemo.
They are still able to log in and are still shown as collaborator in Cawemo.
An admin has to remove the user from the organization in addition to the deletion on the LDAP server.

## View Projects (Admin Only)

Admins have an overview of all the projects created by all the users.
