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
Catalog projects and templates require a valid Enterprise license.
{{< /note >}}

This view is used to view and edit a template. [Templates](https://docs.camunda.org/manual/latest/modeler/element-templates/) can be synchronized with a local [Camunda Modeler](https://docs.camunda.org/manual/latest/modeler/) instance and can be used to predefine properties for various elements.

The catalog project owner has editing rights and all other organization members have read-only access.

You can delete or duplicate a template via the dropdown menu in the [breadcrumb navigation](../home#navigation).

## Template Creation

A newly created template has some default content that you can extend or override. The predefined values give you a hint on what content needs to be added for each property. Read more in our [documentation about Templates](https://docs.camunda.org/manual/latest/modeler/element-templates/).

## Code Editor

The Template page contains a Code Editor that assists you in writing the JSON. It has syntax highlighting, validation, keyboard shortcuts, and more.

{{<img src="../cawemo-code-editor.png">}}

Templates are saved automatically after every content change and if the JSON is valid.

## Import / Export

You can override a template's content by dragging and dropping a JSON file from your local file system onto the Code Editor. You will be asked to confirm the upload since the changes are permanent and not revertable.

The template can be exported as a JSON file by clicking on the export icon in the upper right corner.
