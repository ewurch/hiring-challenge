from fastapi import FastAPI, HTTPException

from cluster.core import Cluster, Node, Group, find_group

app = FastAPI(
    title="Cluster Management API",
    version="0.1.0"
)

# create connection to cluster
cluster = Cluster()

v1 = FastAPI()

@v1.get("/")
def root():
    return cluster

@v1.post("/node", status_code=201)
def add_node(node: Node):
    cluster.add_node(node)
    return node

@v1.delete("/node")
def remove_node(node: Node):
    cluster.remove_node(node)
    return node

@v1.get("/group/{group_id}")
def get_group(group_id: str):
    try:
        return find_group(cluster, group_id=group_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@v1.post("/group", status_code=201)
def create_group(group: Group):
    try:
        group = cluster.add_group(group=group) 
        return group
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@v1.delete("/group")
def remove_group(group: Group):
    try:
        group = cluster.remove_group(group=group)
        return group
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


app.mount("/v1", v1)
