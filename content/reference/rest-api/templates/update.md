---
title: 'Templates: update'
weight: 10

menu:
  main:
    name: 'update'
    identifier: 'rest-api-templates-update'
    parent: 'rest-api-templates'
    pre: 'Updates a template.'
---

Updates a template.

# Request

## HTTP Request

```
PATCH https://cawemo.com/api/v1/templates/:id
```

## Path Parameters

<table class="table table-striped">
 <tr>
   <th>Name</th>
   <th>Type</th>
   <th>Description</th>
 </tr>
  <tr>
    <td>id</td>
    <td>string</td>
    <td>Unique identifier of the template to update.</td>
  </tr>
</table>

## Request Body

In the request body, supply **only** the properties of a [Templates resource]({{< ref "/reference/rest-api/templates/_index.md#resource-representation" >}}) that you want to update.
The following properties are updatable:

<table class="table table-striped">
  <tr>
    <th>Property Name</th>
    <th>Type</th>
    <th>Description</th>
    <th>Notes</th>
  </tr>
  <tr>
    <td>$schema</td>
    <td>string</td>
    <td>URI pointing towards the JSON schema which defines the structure of the element template .json file. Element template schemas are maintained in the <a href="https://github.com/camunda/element-templates-json-schema">element templates JSON schema repository</a>.</td>
    <td>In case no <i>$schema</i> is defined, Cawemo assumes the latest JSON Schema version.</td>
  </tr>
  <tr>
    <td>appliesTo</td>
    <td>string[]</td>
    <td>List of BPMN types the template can be applied to.</td>
    <td></td>
  </tr>
  <tr>
    <td>description</td>
    <td>string</td>
    <td>Description of the template.</td>
    <td></td>
  </tr>
  <tr>
    <td>metadata.catalogId</td>
    <td>string</td>
    <td>Unique identifier of the catalog project the template's is located in.</td>
    <td></td>
  </tr>
  <tr>
    <td>metadata.published</td>
    <td>boolean</td>
    <td>Whether the current version of the template should be published.</td>
    <td></td>
  </tr>
  <tr>
    <td>metadata.templateVersionName</td>
    <td>boolean</td>
    <td>The name of the published template version.</td>
    <td>Only taken into account in combination with <i>metadata.published: true</i>.</td>
  </tr>
  <tr>
    <td>name</td>
    <td>string</td>
    <td>Name of the template.</td>
    <td></td>
  </tr>
  <tr>
    <td>properties</td>
    <td>object[]</td>
    <td>List of properties of the template, see <a href="https://github.com/camunda/camunda-modeler/tree/master/docs/element-templates#defining-template-properties">the Camunda Modeler documentation</a> for a description.</td>
    <td></td>
  </tr>
  <tr>
    <td>scopes</td>
    <td>object[]</td>
    <td>List of scoped bindings of the template, see <a href="https://github.com/camunda/camunda-modeler/tree/master/docs/element-templates#scoped-bindings">the Camunda Modeler documentation</a> for a description.</td>
    <td></td>
  </tr>
</table>

# Response

If successful, this method returns a [Templates resource]({{< ref "/reference/rest-api/templates/_index.md#resource-representation" >}}) in the response body.
