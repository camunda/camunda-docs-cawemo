---
title: 'Catalog Projects'
weight: 20

menu:
  main:
    identifier: 'rest-api-catalogs'
    parent: 'rest-api'
---

See the list of all available [HTTP methods](#methods) for this resource at end of this page.

# Resource Representation

```json
{
  "created": 1576453532000,
  "id": "6636a1c7-506b-4f00-b336-7f54f6a33ae5",
  "name": "My First Catalog Project",
  "updated": 1608075932000
}
```

<table class="table table-striped">
 <tr>
   <th>Name</th>
   <th>Type</th>
   <th>Description</th>
 </tr>
  <tr>
    <td>created</td>
    <td>date (UNIX Epoch time in milliseconds)</td>
    <td>Creation time of the catalog project.</td>
  </tr>
  <tr>
    <td>id</td>
    <td>string</td>
    <td>Unique identifier of the catalog project.</td>
  </tr>
  <tr>
    <td>name</td>
    <td>string</td>
    <td>Name of the catalog project.</td>
  </tr>
  <tr>
    <td>updated</td>
    <td>date (UNIX Epoch time in milliseconds)</td>
    <td>Time when the catalog project was last updated.</td>
  </tr>
</table>

# Methods
