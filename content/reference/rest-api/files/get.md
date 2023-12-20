---
title: 'Files: get'
weight: 10

menu:
  main:
    name: 'get'
    identifier: 'rest-api-files-get'
    parent: 'rest-api-files'
    pre: 'Gets a file by ID.'
---

Gets the latest version of a file by ID.

# Request

## HTTP Request

```
GET https://cawemo.com/api/v1/files/:id
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
    <td>Unique identifier of the file to request.</td>
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
    <td>Content of the requested file.</td>
  </tr>
  <tr>
    <td>metadata</td>
    <td>object</td>
    <td>Metadata of the file, see <a href="{{< ref "/reference/rest-api/files/_index.md#resource-representation" >}}">File resource</a>.</td>
  </tr>
</table>
