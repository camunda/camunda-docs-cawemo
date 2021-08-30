---
title: 'Process Definitions: create version'
weight: 10

menu:
  main:
    name: 'create version'
    identifier: 'rest-api-process-definitions-create-version'
    parent: 'rest-api-process-definitions'
    pre: 'Creates a process definition version.'
---

Creates a new process definition version.

# Request

## HTTP Request

```
POST https://cawemo.com/api/v1/engine-projects/:engine-project-id/process-definitions/versions
```

## Path Parameters

<table class="table table-striped">
  <tr>
    <th>Name</th>
    <th>Type</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>engine-project-id</td>
    <td>string</td>
    <td>Unique identifier of the engine project that contains the process definition.</td>
  </tr>
</table>

## Request Body

In the request body, supply a [Process Definitions resource]({{< ref "/reference/rest-api/process-definitions/_index.md#resource-representation" >}}) with the following properties:

<table class="table table-striped">
  <tr>
    <th>Property Name</th>
    <th>Type</th>
    <th>Description</th>
    <th>Notes</th>
  </tr>
  <tr>
    <td>content</td>
    <td>string</td>
    <td>The process definition's BPMN 2.0 XML representation.</td>
    <td></td>
  </tr>
  <tr>
    <td>created (optional)</td>
    <td>date (UNIX Epoch time in milliseconds)</td>
    <td>The creation date assigned to the process definition's version.</td>
    <td>Has to lie in the past. Defaults to <i>now</i>.</td>
  </tr>
  <tr>
    <td>version</td>
    <td>number</td>
    <td>The version of the process definition.</td>
    <td></td>
  </tr>
</table>

# Response

If successful, this method returns a [Process Definitions resource]({{< ref "/reference/rest-api/process-definitions/_index.md#resource-representation" >}}) in the response body.
