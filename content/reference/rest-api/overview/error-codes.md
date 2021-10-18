---
title: 'Error Codes'
weight: 20

menu:
  main:
    identifier: 'rest-api-error-codes'
    parent: 'rest-api-overview'
---

Cawemo's public API returns error information as status codes in the response header.
Additionally, it _may_ return a JSON object following the format defined by [RFC 7807](https://tools.ietf.org/html/rfc7807) in the response body with additional details that can help you determine how to handle the error.

This page gives an overview of errors that might occur when accessing the public API.

## 400: Bad Request

A `400` error can result from any one of the following issues in your request:

* A required field or parameter hasn't been provided.
* The value supplied or a combination of provided fields is invalid.

```json
{
  "status": 400,
  "title": "Constraint Violation",
  "type": "https://docs.camunda.org/cawemo/latest/reference/rest-api/overview/error-codes/#400-bad-request",
  "violations": [
    {
      "field": "appliesTo",
      "message": "must not be empty"
    },
    {
      "field": "metadata.templateVersionName",
      "message": "size must be between 1 and 255"
    },
    {
      "field": "name",
      "message": "must not be blank"
    }
  ]
}
```

To fix this error, check the `message` field and adjust your request accordingly.

## 401: Unauthorized

A `401` error indicates that either the basic authentication credentials you're using are invalid or the authorization header is missing.

```json
{
  "detail": "Full authentication is required to access this resource",
  "status": 401,
  "title": "Unauthorized"
}
```

To fix this error, check if your request includes an authorization header with valid credentials.
See [Authentication]({{< ref "authentication.md" >}}) for more information on how to authenticate against the public API.

## 404: Resource Not Found

A `404` error indicates that the authenticated API key does not have the proper access to a resource, or the resource does not exist.

```json
{
  "detail": "Could not find the requested resource.",
  "status": 404,
  "title": "Not Found"
}
```

## 500: Internal Server Error

A `500` error occurs when an unexpected error arises while processing the request.

```json
{
  "detail": "Internal Server Error.",
  "status": 500,
  "title": "Internal Server Error"
}
```
