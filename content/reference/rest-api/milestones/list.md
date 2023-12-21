---
title: 'Milestones: list'
weight: 10

menu:
  main:
    name: 'list'
    identifier: 'rest-api-milestones-list'
    parent: 'rest-api-milestones'
    pre: 'Lists milestones.'
---

Lists all milestones of a file.

# Request

## HTTP Request

```
GET https://cawemo.com/api/v1/files/:id/milestones
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
    <td>Unique identifier of the file of which to list the milestones.</td>
  </tr>
</table>

## Request Body

Do not supply a request body with this method.

# Response

If successful, this method returns an array of [Milestone resources]({{< ref "/reference/rest-api/milestones/_index.md#resource-representation" >}}) in the response body.
