from fastapi import FastAPI, HTTPException

from cluster.core import cluster, Group, find_group

app = FastAPI(
    title="Cluster Management API",
    version="0.1.0"
)

v1 = FastAPI()

@v1.get("/", tags=["Cluster"])
def root():
    return cluster

@v1.get("/group/{group_id}", status_code=200, tags=["Cluster"])
def get_group(group_id: str):
    """
    """
    try:
        return find_group(cluster, group_id=group_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@v1.delete("/group", status_code=200, tags=["Cluster"])
def delete_group(group: Group):
    try:
        group = cluster.delete_group_from_cluster(group=group)
        return group
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@v1.post("/group", status_code=201, tags=["Cluster"])
def create_group(group: Group):
    try:
        group = cluster.add_group_to_cluster(group=group) 
        return group
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

app.mount("/v1", v1)
