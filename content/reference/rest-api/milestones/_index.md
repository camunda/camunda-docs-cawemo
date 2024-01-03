---
title: 'Milestones'
weight: 40

menu:
  main:
    identifier: 'rest-api-milestones'
    parent: 'rest-api'
---

See the list of all available [HTTP methods](#methods) for this resource at end of this page.

# Resource Representation

```json
{
  "created": "2019-12-15T23:45:32.000Z",
  "createdBy": {
    "id": "4975a794-26b0-47a9-b953-a57bb2dc5719",
    "name": "foo"
  },
  "fileId": "c7385b2e-14ac-42b5-98fc-3c960201134c",
  "id": "def751d7-eccd-4f94-952e-f62988cef786",
  "name": "My First Milestone",
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
    <td>created</td>
    <td>date (in ISO-8601 format)</td>
    <td>Creation date and time of the milestone.</td>
  </tr>
  <tr>
    <td>createdBy.id</td>
    <td>string</td>
    <td>Unique identifier of the user who created the milestone.</td>
  </tr>
  <tr>
    <td>createdBy.name</td>
    <td>string</td>
    <td>Name of the user who created the milestone.</td>
  </tr>
  <tr>
    <td>fileId</td>
    <td>string</td>
    <td>Unique identifier of the parent file.</td>
  </tr>
  <tr>
    <td>id</td>
    <td>string</td>
    <td>Unique identifier of the milestone.</td>
  </tr>
  <tr>
    <td>name</td>
    <td>string</td>
    <td>Name of the milestone.</td>
  </tr>
  <tr>
    <td>updated</td>
    <td>date (in ISO-8601 format)</td>
    <td>Date and time when the milestone was last updated.</td>
  </tr>
  <tr>
    <td>updatedBy.id</td>
    <td>string</td>
    <td>Unique identifier of the user who last updated the milestone.</td>
  </tr>
  <tr>
    <td>updatedBy.name</td>
    <td>string</td>
    <td>Name of the user who last updated the milestone.</td>
  </tr>
</table>

# Methods
