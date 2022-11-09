from pydantic import BaseModel

class Group(BaseModel):
    groupID: str

class Node(BaseModel):
    url: str
    groups: list[Group] = []

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

    def get_group(self, group_id: str) -> Group:
        for group in self.nodes[0].groups:
            if group.groupID == group_id:
                return group
        raise Exception("Group not found")

    def delete_group(self, group_id: str) -> None:
        for node in self.nodes:
            for group in node.groups:
                if group.groupID == group_id:
                    node.groups.remove(group)
                    deleted_group = group
        print(f"Group {group_id} removed from all nodes")
        return deleted_group

    def create_group(self, group: Group) -> None:
        if self.validate_cluster_consisitency():
            for node in self.nodes:
                node.groups.append(group)
            print(f"Group {group.groupID} added to all nodes")
        else:
            self.rollback_cluster()
            raise Exception("Cluster is not consistent, performing rollback")




cluster = Cluster()

HOSTS = [
    'node1.example.com',
    'node2.example.com',
    'node3.example.com',
]
for host in HOSTS:
    cluster.add_node(url=host)

cluster.create_group(Group(groupID='group1'))
cluster.create_group(Group(groupID='group2'))
