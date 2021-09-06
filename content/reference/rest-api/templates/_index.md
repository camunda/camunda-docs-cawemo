---
title: 'Templates'
weight: 30

menu:
  main:
    identifier: 'rest-api-templates'
    parent: 'rest-api'
---

See the list of all available [HTTP methods](#methods) for this resource at end of this page.

# Resource Representation

```json
{
  "$schema": "https://unpkg.com/@camunda/element-templates-json-schema@0.4.0/resources/schema.json",
  "appliesTo": [
    "bpmn:ServiceTask"
  ],
  "description": "This is my first template.",
  "id": "4f50eb6b-89c7-4684-8b61-228af15cf60c",
  "metadata": {
    "catalogId": "f0291afa-2071-4494-99cd-09c8bb1af2c9",
    "created": 1576453532000,
    "published": true,
    "tags": [
      "My First Catalog Project"
    ],
    "templateVersionName": "My First Template Version",
    "updated": 1608075932000
  },
  "name": "My First Template",
  "properties": [],
  "scopes": [],
  "version": 1576453532000
}
```

See also [the Camunda Modeler documentation](https://github.com/camunda/camunda-modeler/tree/master/docs/element-templates#defining-templates) for a description of template descriptor.

<table class="table table-striped">
  <tr>
    <th>Property Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>$schema</td>
    <td>string</td>
    <td>URI pointing towards the JSON schema which defines the structure of the element template .json file. Element template schemas are maintained in the <a href="https://github.com/camunda/element-templates-json-schema">element templates JSON schema repository</a>.</td>
  </tr>
  <tr>
    <td>appliesTo</td>
    <td>string[]</td>
    <td>List of BPMN types the template can be applied to.</td>
  </tr>
  <tr>
    <td>description</td>
    <td>string</td>
    <td>Description of the template.</td>
  </tr>
  <tr>
    <td>id</td>
    <td>string</td>
    <td>Unique identifier of the template.</td>
  </tr>
  <tr>
    <td>metadata.catalogId</td>
    <td>string</td>
    <td>Unique identifier of the catalog project the template is located in.</td>
  </tr>
  <tr>
    <td>metadata.created</td>
    <td>date (UNIX Epoch time in milliseconds)</td>
    <td>Creation time of the template version.</td>
  </tr>
  <tr>
    <td>metadata.published</td>
    <td>boolean</td>
    <td>Whether the returned version of the template is published or not.</td>
  </tr>
  <tr>
    <td>metadata.templateVersionName</td>
    <td>boolean</td>
    <td>The name of the template version.</td>
  </tr>
  <tr>
    <td>metadata.updated</td>
    <td>date (UNIX Epoch time in milliseconds)</td>
    <td>Time when the template version was last updated.</td>
  </tr>
  <tr>
    <td>name</td>
    <td>string</td>
    <td>Name of the template.</td>
  </tr>
  <tr>
    <td>properties</td>
    <td>object[]</td>
    <td>List of properties of the template, see <a href="https://github.com/camunda/camunda-modeler/tree/master/docs/element-templates#defining-template-properties">the Camunda Modeler documentation</a> for a description.</td>
  </tr>
  <tr>
    <td>scopes</td>
    <td>object[]</td>
    <td>List of scoped bindings of the template, see <a href="https://github.com/camunda/camunda-modeler/tree/master/docs/element-templates#scoped-bindings">the Camunda Modeler documentation</a> for a description.</td>
  </tr>
  <tr>
    <td>version</td>
    <td>date (UNIX Epoch time in milliseconds)</td>
    <td>Creation time of the template version.</td>
  </tr>
</table>

# Methods
