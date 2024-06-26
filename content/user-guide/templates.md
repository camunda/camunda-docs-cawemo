---
title: 'Templates'
weight: 60

menu:
  main:
    identifier: 'templates'
    parent: 'user-guide'
    Pre: ""
---

This view is used to display and edit a template. [Templates](https://docs.camunda.org/manual/latest/modeler/element-templates/) can be synchronized with a local [Camunda Modeler](https://docs.camunda.org/manual/latest/modeler/) instance and can be used to predefine properties for BPMN elements like service tasks.

Only the catalog project owner can edit or delete a template, while all other organization members have read-only access.

You can delete, duplicate, or rename a template via the dropdown menu in the [breadcrumb navigation](../home#navigation).

## Template Types

Cawemo currently supports two types of templates:

 * **Service Task templates** represent external service tasks which run outside the process engine's boundaries. They can be edited using the [form-based editor](#service-task-template-editor), and you can choose between three implementation types
   * External Service Task
   * RPA Bridge Task - UiPath
   * RPA Bridge Task - Automation Anywhere
 * **Generic JSON templates** are general purpose templates not bound to a specific use case. New templates are created with a default content that you can extend or override. The default values give you a hint on what content needs to be added for each property. Read more in our [documentation about templates](https://docs.camunda.org/manual/latest/modeler/element-templates/).

## Service Task Template Editor

The Service Task template editor provides a form in which you can easily define the required parameters for the chosen implementation type. You can read more about this in the documentation about [External Tasks](https://docs.camunda.org/manual/latest/user-guide/process-engine/external-tasks) and the [Camunda RPA Bridge](https://docs.camunda.org/manual/latest/user-guide/camunda-bpm-rpa-bridge). Additionally, there is the possibility to define [BPMN Errors](https://docs.camunda.org/manual/latest/user-guide/camunda-bpm-rpa-bridge/#error-handling) which are thrown when the External Task or RPA Bridge Task fails for any reason.

In the background Cawemo ensures that a valid template JSON is produced and offered to the Camunda Modeler user. You can also inspect the generated JSON by clicking the "Show Code Editor" button in the upper right corner.

{{<img src="../template-form-editor.png">}}

**Please note**: If you start editing the JSON code of a Service Task template, it will be converted to a generic template and the form editor can no longer be used for it.

### Service Task Template Actions

In the upper right corner of the template editor, the following actions are available:

* Show code editor
* Show version history
* Download JSON
* Open guide
* Publish

## Code Editor

The code editor assists you in writing templates in JSON text format. It has syntax highlighting, validation, keyboard shortcuts, and more. Templates are saved automatically after every content change if you have typed in valid (syntactically correct) JSON.

{{<img src="../template-code-editor.png">}}

### Generic JSON Template Actions

In the upper right corner of the code editor, the following actions are available:

* Show version history
* Download JSON
* Open guide
* Publish

## Publishing and Version History

Before a template can be used in the Camunda Modeler it needs to be published once by clicking the "Publish" button in the upper right corner. If you like you can provide a name for the published version. In case you need to adjust your template later on, you can simply publish a new version of it.

The version history, available from template actions or the breadcrumb menu, shows all published versions and allows you to keep track of the changes. Within the version history, the latest version can directly be published. 

Template versions work similar to [milestones](../milestones) for diagrams.

## Import / Export

You can override a template's content by dragging and dropping a template JSON file from your local file system onto the code editor. You will be asked to confirm the upload since the changes are permanent and not revertable.

The template can be exported as a JSON file by clicking on the export icon in the upper right corner.
