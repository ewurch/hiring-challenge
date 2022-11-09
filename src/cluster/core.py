from itertools import chain
from random import choice
from typing import Callable
from pydantic import BaseModel, Field, validator

class Group(BaseModel):
    groupID: str = Field(..., min_length=1)

class Node(BaseModel):
    url: str = Field(..., min_length=1)
    groups: list[Group] = []

    @validator('groups')
    def unique_group_ids(cls, groups: list[Group]) -> list[Group]:
        if len(groups) != len(set([group.groupID for group in groups])):
            raise Exception("Group IDs must be unique")
        return groups

    def add_group(self, group: Group) -> Group:
        if group not in self.groups:
            self.groups.append(group)
            return group
        else:
            raise Exception("group already exists")

    def remove_group(self, group: Group) -> Group:
        if group in self.groups:
            self.groups.remove(group)
            return group
        else:
            raise Exception("Group does not exist in node")

    def get_group_ids(self) -> list[str]:
        return [group.groupID for group in self.groups]

class Cluster(BaseModel):
    nodes: list[Node] = []
    
    @validator('nodes')
    def unique_node_urls(cls, nodes: list[Node]) -> list[Node]:
        if len(nodes) != len(set([node.url for node in nodes])):
            raise Exception("Node URLs must be unique")
        return nodes

    def validate_consistency(self) -> bool:
        # Check if all nodes have the same groups
        for node in self.nodes:
            if node.groups != self.nodes[0].groups:
                return False
        return True

    def rollback(self) -> None:
        # Rollback all nodes to commom state
        n_nodes = len(self.nodes)
        all_groups = list(chain(*[node.groups for node in self.nodes]))
        print(self.nodes)
        for node in self.nodes:
            print(node.groups)
            for group in node.groups:
                message = f"{node.url} - {group.groupID} - {all_groups.count(group)}"
                if all_groups.count(group) != n_nodes:
                    node.remove_group(group)
                    print(message + "- deleted")
                else:
                    print(message + "- kept")

    def check_consistency(func: Callable) -> Callable:
        """Decorator to check if cluster is consistent before performing an operation"""
        def wrapper(*args, **kwargs):
            if args[0].validate_consistency():
                return func(*args, **kwargs)
            else:
                args[0].rollback()
                raise Exception("Cluster is not consistent, rollback performed")
        return wrapper

    @check_consistency
    def add_node(self, node: Node) -> None:
        if node not in self.nodes:
            self.nodes.append(node)
        else:
            raise Exception("Node already exists")

    @check_consistency
    def remove_node(self, node: Node) -> None:
        if node in self.nodes:
            self.nodes.remove(node)
        else:
            raise Exception("Node does not exist")

    @check_consistency
    def add_group(self, group: Group):
        for node in self.nodes:
                node.add_group(group)
        print(f"Group {group.groupID} added to all nodes")
        return group

    @check_consistency
    def remove_group(self, group: Group):
        for node in self.nodes:
            node.remove_group(group)
        print(f"Group {group} removed from all nodes")
        return group


def find_group(cluster: Cluster, group_id: str) -> Group:
    for group in choice(cluster.nodes).groups:
        if group.groupID == group_id:
            return group
    raise Exception(f"Group {group_id} not found in cluster")
