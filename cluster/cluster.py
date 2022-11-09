from pydantic import BaseModel

class Group(BaseModel):
    groupID: str

class Node(BaseModel):
    url: str
    groups: list[Group]

class Cluster(BaseModel):
    nodes: list[Node]
