---
title: 'Engine Projects: list'
weight: 10

menu:
  main:
    name: 'list'
    identifier: 'rest-api-engine-projects-list'
    parent: 'rest-api-engine-projects'
    pre: 'Lists engine projects.'
---

Lists the engine projects with optional query parameters for filtering.

# Request

## HTTP Request

```
GET https://cawemo.example.com/api/v1/engine-projects
```

## Query Parameters

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>name (optional)</td>
    <td>string</td>
    <td>Filter by engine project name.</td>
  </tr>
</table>

# Response

If successful, this method returns an array of [Engine Projects resources]({{< ref "/reference/rest-api/engine-projects/_index.md#resource-representation" >}}) in the response body.
