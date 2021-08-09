---
title: 'Templates: list'
weight: 10

menu:
  main:
    name: 'list'
    identifier: 'rest-api-templates-list'
    parent: 'rest-api-templates'
    pre: 'Lists templates.'
---

Lists the latest version of templates with optional query parameters for filtering.

# Request

## HTTP Request

```
GET https://cawemo.com/api/v1/templates
```

## Query Parameters

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>catalogId (optional)</td>
    <td>string</td>
    <td>Filter by catalog project id.</td>
  </tr>
  <tr>
    <td>includeUnpublishedVersions (optional)</td>
    <td>boolean</td>
    <td>If set to <i>true</i> unpublished versions of a template will be taken into consideration.</td>
  </tr>
</table>

## Request Body

Do not supply a request body with this method.

# Response

If successful, this method returns an array of [Templates resources]({{< ref "/reference/rest-api/templates/_index.md#resource-representation" >}}) in the response body.
