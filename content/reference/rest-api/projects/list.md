---
title: 'Projects: list'
weight: 10

menu:
  main:
    name: 'list'
    identifier: 'rest-api-projects-list'
    parent: 'rest-api-projects'
    pre: 'Lists projects.'
---

Lists all projects in the organization.

# Request

## HTTP Request

```
GET https://cawemo.com/api/v1/projects
```

## Request Body

Do not supply a request body with this method.

# Response

If successful, this method returns an array of [Project resources]({{< ref "/reference/rest-api/projects/_index.md#resource-representation" >}}) in the response body.
