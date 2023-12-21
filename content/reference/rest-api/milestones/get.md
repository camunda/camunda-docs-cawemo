---
title: 'Milestones: get'
weight: 10

menu:
  main:
    name: 'get'
    identifier: 'rest-api-milestones-get'
    parent: 'rest-api-milestones'
    pre: 'Gets a milestone by ID.'
---

Gets a milestone by ID.

# Request

## HTTP Request

```
GET https://cawemo.com/api/v1/milestones/:id
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
    <td>Unique identifier of the milestone to request.</td>
  </tr>
</table>

## Request Body

Do not supply a request body with this method.

# Response

If successful, this method returns the following response body:

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>content</td>
    <td>string</td>
    <td>Content of the requested milestone.</td>
  </tr>
  <tr>
    <td>metadata</td>
    <td>object</td>
    <td>Metadata of the milestone, see <a href="{{< ref "/reference/rest-api/milestones/_index.md#resource-representation" >}}">Milestone resource</a>.</td>
  </tr>
</table>
