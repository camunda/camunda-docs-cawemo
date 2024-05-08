---
title: 'Engine Projects: create'
weight: 10

menu:
  main:
    name: 'create'
    identifier: 'rest-api-engine-projects-create'
    parent: 'rest-api-engine-projects'
    pre: 'Creates or updates an engine project.'
---

Creates or updates an engine project.

# Request

## HTTP Request

```
POST https://cawemo.example.com/api/v1/engine-projects
```

## Request Body

In the request body, supply a [Engine Projects resource]({{< ref "/reference/rest-api/engine-projects/_index.md#resource-representation" >}}) with the following properties:

<table class="table table-striped">
  <tr>
    <th>Property Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>name</td>
    <td>string</td>
    <td>Name of the engine project.</td>
  </tr>
</table>

# Response

If successful, this method returns an [Engine Projects resource]({{< ref "/reference/rest-api/engine-projects/_index.md#resource-representation" >}}) in the response body.
