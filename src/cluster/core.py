from random import choice
from pydantic import BaseModel, conlist

class Group(BaseModel):
    groupID: str

class Node(BaseModel):
    url: str
    groups: list[Group] = []

    def add_group_to_node(self, group: Group):
        if group not in self.groups:
            self.groups.append(group)
        else:
            raise Exception("group already exists")

    def delete_group_from_node(self, group: Group):
        if group in self.groups:
            self.groups.remove(group)
        else:
            raise Exception("Group does not exist in node")

class Cluster(BaseModel):
    nodes: list[Node] = []

    def validate_cluster_consisitency(self) -> bool:
        # Check if all nodes have the same groups
        for node in self.nodes:
            if node.groups != self.nodes[0].groups:
                return False
        return True

    def rollback_cluster(self) -> None:
        # Rollback all nodes to commom state
        pass 

    def add_node(self, url: str) -> None:
        self.nodes.append(Node(url=url, groups=[]))

    def delete_group_from_cluster(self, group: Group):
        for node in self.nodes:
            node.delete_group_from_node(group)
        print(f"Group {group} removed from all nodes")
        return group

    def add_group_to_cluster(self, group: Group):
        for node in self.nodes:
            node.add_group_to_node(group)
        print(f"Group {group.groupID} added to all nodes")
        return group


def find_group(cluster: Cluster, group_id: str) -> Group:
    for group in choice(cluster.nodes).groups:
        if group.groupID == group_id:
            return group
    raise Exception(f"Group {group_id} not found in cluster")

cluster = Cluster()

HOSTS = [
    'node1.example.com',
    'node2.example.com',
    'node3.example.com',
]
for host in HOSTS:
    cluster.add_node(url=host)

cluster.add_group_to_cluster(Group(groupID='group1'))
cluster.add_group_to_cluster(Group(groupID='group2'))
