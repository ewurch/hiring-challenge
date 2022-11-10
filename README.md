Hiring Challenge 
===========
[![Tests](https://github.com/ewurch/swisscom-challenge/actions/workflows/main.yml/badge.svg)](https://github.com/ewurch/swisscom-challenge/actions/workflows/main.yml/)

## Rationale

### The cluster
The approach I took was to build a theoretical cluster of nodes, using Pydantic models I could enforce type hints and create custom validations for each one of the components. Since the Pydantic BaseModel is an extension of dataclasses, i could still build methods for each one of the classes, keeping the componentes with their own responsabilites (data manipulation, data validations and cluster consistency enforcement in the case of instabilities and connection timeouts).

### The API
To Interact with the cluster I built an interface using FastAPI, it's integration with Pydantic allows for type hints on the endpoint definition and interactive docs at the `/v1/docs`.

> Excerpt from the task:
```python
 HOSTS = [
    'node1.example.com',
    'node2.example.com',
    'node3.example.com',
]
```
For complexity and realiability the API still doesn't support batch, operations as the example on the hiring challenge document, each one of the nodes has to be added separately. The same is true for the Groups.


## Building and Running

The project was built using poetry for dependency management.

So all the dependencies are on the poetry files and to run the app is recommended to use the `docker-compose.yml` or the `Dockerfile` directly.

## Usage Guide:
Once the API is running is possible to interact with the cluster, the cluster is not persistent so on each startup you get an empty cluster to interact with.

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

Besides that is still possible to add more nodes and more groups, each time the API has any interaction with the cluster, the cluster self validates for consistency. 

## Testing and CI/CD

The project has >95% test coverage and Test pipeline configured to run on Github Actions 

## Future Improvements

I would say the cluster management architecture is pretty solid, there is more room for improvement on the API side. Supporting batch operations


## Contributing

Feel free to contribute :smiley:
