import pytest

from fastapi.testclient import TestClient

from cluster.core import Cluster, Node, Group 
from api.main import app

client = TestClient(app)

def test_root():
    response = client.get("/v1/")
    assert response.status_code == 200

def test_add_one_node():
    response = client.post("/v1/node", json={"url": "test.node_1.com"})
    assert response.status_code == 201

def test_add_two_nodes():
    response = client.post("/v1/node", json={"url": "test.node_2.com"})
    cluster = Cluster(nodes=[Node(url="test.node_1.com"), Node(url="test.node_2.com")])
    assert response.status_code == 201
    assert cluster == Cluster.parse_obj(client.get('/v1/').json())

def test_remove_node():
    _ = client.delete("/v1/node", json={"url": "test.node_2.com"})
    cluster = Cluster(nodes=[Node(url="test.node_1.com")])
    assert cluster == Cluster.parse_obj(client.get("/v1/").json())

def test_create_group():
    response = client.post("/v1/group", json={"groupID": "group_1"})
    cluster = Cluster(nodes=[Node(url="test.node_1.com", groups=[Group(groupID="group_1")])])
    assert response.status_code == 201
    assert cluster == Cluster.parse_obj(client.get('/v1/').json())

def test_add_existing_group():
    response = client.post("/v1/group", json={"groupID": "group_1"})
    assert response.status_code == 400
    
def test_get_group():
    response = client.get("/v1/group/group_1")
    assert response.status_code == 200
    assert response.json() == {"groupID": "group_1"}

def test_get_non_existing_group():
    response = client.get("/v1/group/group_3")
    assert response.status_code == 404

def test_remove_group():
    _ = client.post("/v1/group", json={"groupID": "group_2"})
    _ = client.delete("/v1/group", json={"groupID": "group_1"})
    cluster = Cluster(nodes=[Node(url="test.node_1.com", groups=[Group(groupID="group_2")])])
    assert cluster == Cluster.parse_obj(client.get("/v1/").json())

def test_remove_non_existing_group():
    response = client.delete("/v1/group", json={"groupID": "group_3"})
    assert response.status_code == 400