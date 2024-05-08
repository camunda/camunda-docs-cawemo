---
title: 'Templates: get'
weight: 10

menu:
  main:
    name: 'get'
    identifier: 'rest-api-templates-get'
    parent: 'rest-api-templates'
    pre: 'Gets a template by ID.'
---

Gets the latest version of a template by ID with optional query parameters for filtering.

# Request

## HTTP Request

```
GET https://cawemo.example.com/api/v1/templates/:id
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
    <td>Unique identifier of the template to request.</td>
  </tr>
</table>

## Query Parameters

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>includeUnpublishedVersions (optional)</td>
    <td>boolean</td>
    <td>If set to <i>true</i> unpublished versions of the template will be taken into consideration.</td>
  </tr>
</table>

## Request Body

Do not supply a request body with this method.

# Response

If successful, this method returns a [Templates resource]({{< ref "/reference/rest-api/templates/_index.md#resource-representation" >}}) in the response body.
