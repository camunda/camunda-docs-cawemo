---
title: 'Process Definitions: versions'
weight: 10

menu:
  main:
    name: 'versions'
    identifier: 'rest-api-process-definitions-versions'
    parent: 'rest-api-process-definitions'
    pre: 'Lists all available versions of a process definition.'
---

Lists all available versions of an engine project.

# Request

## HTTP Request

```
GET https://cawemo.com/api/v1/engine-projects/:engine-project-id/process-definitions/:process-definition-key/versions
```

## Path Parameters

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>engine-project-id</td>
    <td>string</td>
    <td>Unique identifier of the engine project that contains the process definition.</td>
  </tr>
  <tr>
    <td>process-definition-key</td>
    <td>string</td>
    <td>Key of the process definition the versions are requested for.</td>
  </tr>
</table>

# Response

If successful, this method returns an array of [Process Definitions resources]({{< ref "/reference/rest-api/process-definitions/_index.md#resource-representation" >}}) **without the content field** in the response body.
