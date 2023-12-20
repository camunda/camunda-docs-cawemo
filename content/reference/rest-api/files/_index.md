---
title: 'Files'
weight: 30

menu:
  main:
    identifier: 'rest-api-files'
    parent: 'rest-api'
---

See the list of all available [HTTP methods](#methods) for this resource at end of this page.

# Resource Representation

```json
{
  "canonicalPath": [
    {
      "id": "ccf4c1b7-4f36-4282-8beb-b66823285797",
      "name": "My Folder"
    }
  ],
  "created": "2019-12-15T23:45:32.000Z",
  "createdBy": {
    "id": "4975a794-26b0-47a9-b953-a57bb2dc5719",
    "name": "foo"
  },
  "folderId": "c7385b2e-14ac-42b5-98fc-3c960201134c",
  "id": "def751d7-eccd-4f94-952e-f62988cef786",
  "name": "My First File",
  "projectId": "6e1b3175-3b6c-4fc4-9af5-36081d6428c0",
  "revision": 1,
  "type": "BPMN",
  "simplePath": "My Folder/My First File.bpmn",
  "updated": "2020-12-15T23:45:32.000Z",
  "updatedBy": {
    "id": "c8bc0a6a-13bb-49ad-9fcd-60a9a0c4b411",
    "name": "bar"
  }
}
```

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>canonicalPath</td>
    <td>object[]</td>
    <td>Contains the unique path of the file within the project. It is an array of objects representing folders which contain the id and the name of each path element.</td>
  </tr>
  <tr>
    <td>created</td>
    <td>date (in ISO-8601 format)</td>
    <td>Creation date and time of the file.</td>
  </tr>
  <tr>
    <td>createdBy.id</td>
    <td>string</td>
    <td>Unique identifier of the user who created the file.</td>
  </tr>
  <tr>
    <td>createdBy.name</td>
    <td>string</td>
    <td>Name of the user who created the file.</td>
  </tr>
  <tr>
    <td>folderId (optional)</td>
    <td>string</td>
    <td>Unique identifier of the parent folder the file is located in.</td>
  </tr>
  <tr>
    <td>id</td>
    <td>string</td>
    <td>Unique identifier of the file.</td>
  </tr>
  <tr>
    <td>name</td>
    <td>string</td>
    <td>Name of the file.</td>
  </tr>
  <tr>
    <td>projectId</td>
    <td>string</td>
    <td>Unique identifier of the project the file is located in.</td>
  </tr>
  <tr>
    <td>simplePath</td>
    <td>string</td>
    <td>Contains the human-readable path of the file within the project.</td>
  </tr>
  <tr>
    <td>revision</td>
    <td>number</td>
    <td>Revision of the file.</td>
  </tr>
  <tr>
    <td>type</td>
    <td>number</td>
    <td>Type of the file.<br/>Possible values: <i>BPMN</i>, <i>DMN</i>, <i>TEMPLATE_GENERIC</i>, or <i>TEMPLATE_SERVICE_TASK</i>.</td>
  </tr>
  <tr>
    <td>updated</td>
    <td>date (in ISO-8601 format)</td>
    <td>Date and time when the file was last updated.</td>
  </tr>
  <tr>
    <td>updatedBy.id</td>
    <td>string</td>
    <td>Unique identifier of the user who last updated the file.</td>
  </tr>
  <tr>
    <td>updatedBy.name</td>
    <td>string</td>
    <td>Name of the user who last updated the file.</td>
  </tr>
</table>

# Methods
