---
title: 'Templates'
weight: 50

menu:
  main:
    identifier: 'templates'
    parent: 'user-guide'
    Pre: ""
---

{{< note title="Heads Up!" class="warning" >}}
Catalogs and templates are part of the Enterprise license.
{{< /note >}}

This view is used to view and edit a JSON template. Only the catalog owner has editing rights; all other organization members only have read-only access.

You can delete or duplicate the template through the dropdown menu in the [breadcrumb navigation](../home#navigation).

## Template Creation

A newly created template will already have some default content that you can extend or override. The predefined values give you a hint on what content needs to be added for each property. For further documentation about Element templates, [click here](https://docs.camunda.org/manual/latest/modeler/element-templates/).

## Code Editor

The Template page contains a Code Editor that assists you in writing the JSON. It has syntax highlighting, validation, keyboard shortcuts, and more.

{{<img src="../cawemo-code-editor.png">}}

Templates are saved automatically after the content has changed, but won't save if the JSON is invalid (like a missing comma).

## Import / Export

You can override a template's content by dragging and dropping a JSON file from your local file system onto the Code Editor. You will be asked to confirm the upload since the changes are permanent and not revertable.

The template can be exported as a JSON file by clicking on the export icon in the upper right corner.