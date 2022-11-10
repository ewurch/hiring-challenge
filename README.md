Hiring Challenge 
===========
[![Tests](https://github.com/ewurch/swisscom-challenge/actions/workflows/main.yml/badge.svg)](https://github.com/ewurch/swisscom-challenge/actions/workflows/main.yml/)

## Rationale

### The cluster
The approach I took was to build a theoretical cluster of nodes, using Pydantic models I could enforce type hints and create custom validations for each one of the components. Since the Pydantic BaseModel is an extension of python's dataclasses, I could still build methods for each one of the classes, keeping the components with their own responsibilities (data manipulation, data validations, and cluster consistency enforcement in the case of instabilities and connection timeouts).

### The API
To Interact with the cluster I built an interface using FastAPI, it's integration with Pydantic allows for type hints on the endpoint definition and interactive docs at the `/v1/docs`.


## Building and Running

The project was built using poetry for dependency management.

So all the dependencies are on the poetry files and to run the app is recommended to use the `docker-compose.yml` or the `Dockerfile` directly.

## Usage Guide:
Once the API is running is possible to interact with the cluster, the cluster is not persistent so on each startup you get an empty cluster to interact with.

On this usage guide you will learn how to interact with the API using the requests library, but is also possible to use it through the interface provided on `/v1/docs`.

```python
>>> import requests
>>> response = requests.get('http://localhost:8000/v1/')
>>> response.json()
{'nodes': []}
```
### Adding a Node
```python
>>> r = requests.post('http://localhost:8000/v1/node', json={'url':'node1.example.com'})
>>> r.json()
{'url': 'node1.example.com', 'groups': []}
```

### Adding a Group
```python
>>> r = requests.post('http://localhost:8000/v1/group', json={'groupID':'1'})
>>> r.json()
{'groupID': '1'}
```


### Retrieving a Group
```python
>>> r = requests.get('http://localhost:8000/v1/group/1')
>>> r.json()
{'groupID': '1'}
```

---

Besides that, it is still possible to add more nodes and more groups, each time the API has any interaction with the cluster, the cluster self-validates for consistency. 

## Testing and CI/CD

The project has >90% test coverage and a test pipeline configured to run on GitHub Actions 

## Future Improvements

I would say the cluster management architecture is pretty solid, there is more room for improvement on the API side. For complexity and reliability the API still doesn't support batch operations as the example on the hiring challenge document:

> Excerpt from the task:
```python
 HOSTS = [
    'node1.example.com',
    'node2.example.com',
    'node3.example.com',
]
```
Each one of the nodes has to be added separately. The same is true for the Groups.

The docs are written on the functions, 

## Contributing

Feel free to contribute :smiley:
