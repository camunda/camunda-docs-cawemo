---
title: 'Projects'
weight: 20

menu:
  main:
    identifier: 'projects'
    parent: 'user-guide'
    Pre: "Shows the content of a project and the list of collaborators"
---

This view shows the content of a project and the list of collaborators.

## Collaboration / Access Rights 

### Projects created from Cawemo

After creating a project, further Cawemo users can be invited to collaborate.
There are four roles with different levels of access rights that can be assigned to each user:

- **Project Admin:** the user can edit the project itself, all folders and diagrams within the project and invite further users.
- **Editor:** the user can edit all folders and diagrams within the project.
- **Commenter:** the user cannot edit folders or diagrams nor invite users, but can leave [comments](../diagrams#comments) on each diagram.
- **Viewer:** the user cannot edit folders or diagrams nor leave comments, but only view diagrams.

The **Project Admin** is the only user entitled to invite and manage user roles.

On the Home Page you are able to easily identify who has access to the project:

{{<img src="../default-project.png" title="Project created from Cawemo - collaborators visibility" width="150%" height="150%">}}

{{< note class="info" >}}
When there are more than a handful of users, you can hover over the circle with a number on it to view the names of all users that have access.
{{< /note >}}

### Projects used by integrations

Projects used by integrations do not allow you to manage access rights.
All [members of your organization](../settings#managing-members-admin-only) automatically gain _read-only_ access to your catalog, engine and modeler projects, meaning that they can see your files, but not edit them.

On the Home Page you are able to easily identify who has access to the project. In this case: **Everyone** in the organization has access:
{{<img src="../integration-projects.png" title="Projects created via integrations - collaborators visibility" width="150%" height="150%">}}

## Import

Diagrams can be added to a project by dragging and dropping a BPMN or DMN XML file from the local file system onto the list of diagrams in the project.
