---
title: 'Files: list'
weight: 10

menu:
  main:
    name: 'list'
    identifier: 'rest-api-files-list'
    parent: 'rest-api-files'
    pre: 'Lists files.'
---

Lists all files within a project.

# Request

## HTTP Request

```
GET https://cawemo.com/api/v1/projects/:id/files
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
    <td>Unique identifier of the project of which to list the files.</td>
  </tr>
</table>

## Request Body

Do not supply a request body with this method.

# Response

If successful, this method returns an array of [File resources]({{< ref "/reference/rest-api/files/_index.md#resource-representation" >}}) in the response body.
