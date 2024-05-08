---
title: 'Milestones: create'
weight: 10

menu:
  main:
    name: 'create'
    identifier: 'rest-api-milestones-create'
    parent: 'rest-api-milestones'
    pre: 'Creates a new milestones.'
---

Creates a new milestone.

# Request

## HTTP Request

```
POST https://cawemo.example.com/api/v1/milestones
```

## Request Body

In the request body, supply a [Milestones resource]({{< ref "/reference/rest-api/milestones/_index.md#resource-representation" >}}) with the following properties:

<table class="table table-striped">
  <tr>
    <th>Property Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>fileId</td>
    <td>string</td>
    <td>Unique identifier of the file to create the milestone for.</td>
  </tr>
  <tr>
    <td>name</td>
    <td>string</td>
    <td>Name of the milestone to create.</td>
  </tr>
</table>

# Response

If successful, this method returns a [Milestone resource]({{< ref "/reference/rest-api/milestones/_index.md#resource-representation" >}}) in the response body.
