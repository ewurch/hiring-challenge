from pydantic import BaseModel

class Node(BaseModel):
    url: str

class Cluster(BaseModel):
    nodes: list[Node]
