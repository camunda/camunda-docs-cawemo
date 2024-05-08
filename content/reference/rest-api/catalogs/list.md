---
title: 'Catalog Projects: list'
weight: 10

menu:
  main:
    name: 'list'
    identifier: 'rest-api-catalogs-list'
    parent: 'rest-api-catalogs'
    pre: 'Lists catalog projects within the organization.'
---

Lists catalog projects within the organization.

# Request

## HTTP Request

```
GET https://cawemo.example.com/api/v1/catalogs
```

# Response

If successful, this method returns an array of [Catalog Project resources]({{< ref "/reference/rest-api/catalogs/_index.md#resource-representation" >}}) in the response body.
