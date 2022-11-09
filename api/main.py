from fastapi import FastAPI

from cluster.core import cluster, Group

app = FastAPI()

v1 = FastAPI()

@v1.get("/")
def root():
    return cluster

@v1.get("/group/{group_id}")
def get_group(group_id: str):
    group = cluster.get_group(group_id=group_id)
    return group

@v1.delete("/group/{group_id}")
def delete_group(group_id: str):
    group = cluster.delete_group(group_id=group_id)
    return group

@v1.post("/group")
def create_group(group: Group):
    cluster = cluster.create_group(group=group) 
    return cluster

app.mount("/v1", v1)