from itertools import chain
from random import choice
from typing import Callable
from pydantic import BaseModel, Field, validator

class Group(BaseModel):
    """Holds a GroupID that will be replicated across all nodes in the cluster"""
    groupID: str = Field(..., min_length=1)

class Node(BaseModel):
    """Has an identifier URL and holds a list of groups, all Nodes on the
    cluster should have the same groups and different URLs"""
    url: str = Field(..., min_length=1)
    groups: list[Group] = []

    @validator('groups')
    def unique_group_ids(cls, groups: list[Group]) -> list[Group]:
        """Ensures that all groups have unique groupIDs on build time"""
        if len(groups) != len(set([group.groupID for group in groups])):
            raise Exception("Group IDs must be unique")
        return groups

    def add_group(self, group: Group) -> Group:
        """Adds a group to the node, if the group already exists, 
        it will raise an exception"""
        if group not in self.groups:
            self.groups.append(group)
            return group
        else:
            raise Exception("group already exists")

    def remove_group(self, group: Group) -> Group:
        """Removes a group from the node, if the group does not exist it will
        raise an exception"""
        if group in self.groups:
            self.groups.remove(group)
            return group
        else:
            raise Exception("Group does not exist in node")

    def get_group_ids(self) -> list[str]:
        """Returns a list of groupIDs for the node"""
        return [group.groupID for group in self.groups]

class Cluster(BaseModel):
    """The cluster is the highest level component of the architecture, it interacts
    with the nodes and make sure that all nodes have the same groups"""
    nodes: list[Node] = []
    
    @validator('nodes')
    def unique_node_urls(cls, nodes: list[Node]) -> list[Node]:
        """Ensures that all nodes have unique URLs on build time"""
        if len(nodes) != len(set([node.url for node in nodes])):
            raise Exception("Node URLs must be unique")
        return nodes

    def validate_consistency(self) -> bool:
        """Validates if all nodes on the cluster have the same groups"""
        # Check if all nodes have the same groups
        for node in self.nodes:
            if node.groups != self.nodes[0].groups:
                return False
        return True

    def rollback(self) -> None:
        """Rolls back the cluster to a consistent state, it is, sets all nodes groups
        to the only ones all nodes have in common
        
        Caution: This method is not stable and should be called several times to ensure
        consistency
        """
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
    def add_node(self, node: Node) -> Node:
        """Adds a node to the cluster, if the node already exists, it will raise an exception"""
        if node not in self.nodes:
            self.nodes.append(node)
            return node
        else:
            raise Exception("Node already exists")

    @check_consistency
    def remove_node(self, node: Node) -> Node:
        """Remove a node to the cluster, if the node doesn't exists, it will raise an exception"""
        if node in self.nodes:
            self.nodes.remove(node)
            return node
        else:
            raise Exception("Node does not exist")

    @check_consistency
    def add_group(self, group: Group):
        """Cluster level interface to add a group to all nodes"""
        for node in self.nodes:
                node.add_group(group)
        print(f"Group {group.groupID} added to all nodes")
        return group

    @check_consistency
    def remove_group(self, group: Group):
        """Cluster level interface to remove a group from all nodes"""
        for node in self.nodes:
            node.remove_group(group)
        print(f"Group {group} removed from all nodes")
        return group


def find_group(cluster: Cluster, group_id: str) -> Group:
    """"Find a group in the cluster by its groupID
    
    Performs a search on all nodes and returns the first group with the given groupID

    Args:
        cluster (Cluster): The cluster to search
        group_id (str): The groupID to search for

    returns:
        Group: The group with the given groupID

    Example:
        >>> cluster = Cluster(nodes=[Node(url="demo.cluster.com", groups=[Group(groupID="group1")])])
        >>> find_group(cluster, "group1")
        Group(groupID='group1')
    """
    for group in choice(cluster.nodes).groups:
        if group.groupID == group_id:
            return group
    raise Exception(f"Group {group_id} not found in cluster")
