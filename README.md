[![Tests](https://github.com/ewurch/swisscom-challenge/workflows/Tests/badge.svg)](https://github.com/ewurch/swisscom-challenge/actions?workflow=Tests)

Hiring Challenge - Swisscom
===========

# Objective summary

## Api consumer

> There is a cluster consisting of several nodes. When you create a group, you need to create a record of it on all nodes via API. When you delete an object, you also need to delete it from all nodes. The problem is that API is unstable. E.g. you can expect connection timeout or 500 errors for unknown reasons. If you got an error, then all changes should be rolled back. 
> You should implement a module that will create and delete objects in the cluster as reliably as possible.`

Create a theoritical cluster that can be configured with this example cluster configuration:

```python
HOSTS = [
    'node1.example.com',
    'node2.example.com',
    'node3.example.com',
]
```

## API

### Create
`URL: /v1/group/` 

`Method: POST`

`Request (application/json):`
```json
{
    "groupId": "str",
}
```