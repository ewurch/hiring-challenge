import pytest

from cluster.core import Group, Node, Cluster, find_group

def test_create_group_with_empty_id():
    with pytest.raises(Exception):
        group = Group(groupID="")

def test_create_group_with_string_id():
    group = Group(groupID="123")
    assert group.groupID == "123"

def test_create_group_with_int_id():
    group = Group(groupID=123)
    assert group.groupID == "123"

def test_create_node_with_empty_node():
    with pytest.raises(Exception):
        node = Node()

def test_create_node_with_empty_groups():
    node = Node(url="test.node.com")
    assert node.groups == []

def test_create_node_with_url_and_groups():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    node = Node(
        url="test.node.com",
        groups=[test_group_1, test_group_2]
    )
    assert node.url == "test.node.com"
    assert node.groups == [test_group_1, test_group_2]

def test_add_group_to_node():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    node = Node(
        url="test.node.com",
        groups=[test_group_1, test_group_2]
    )
    test_group_3 = Group(groupID="group_3")
    node.add_group(test_group_3)
    assert node.groups == [test_group_1, test_group_2, test_group_3]

def test_add_existing_group_to_node():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    node = Node(
        url="test.node.com",
        groups=[test_group_1, test_group_2]
    )
    with pytest.raises(Exception):
        node.add_group_to_node(test_group_1)

def test_remove_group_from_node():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    node = Node(
        url="test.node.com",
        groups=[test_group_1, test_group_2]
    )
    node.remove_group(test_group_1)
    assert node.groups == [test_group_2]

def test_remove_non_existent_group_from_node():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    node = Node(
        url="test.node.com",
        groups=[test_group_1, test_group_2]
    )
    test_group_3 = Group(groupID="group_3")
    with pytest.raises(Exception):
        node.remove_group(test_group_3)

def test_get_group_ids_from_node():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    node = Node(
        url="test.node.com",
        groups=[test_group_1, test_group_2]
    )
    assert node.get_group_ids() == ["group_1", "group_2"]

def test_add_node_to_cluster():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    node = Node(
        url="test.node.com",
        groups=[test_group_1, test_group_2]
    )
    cluster = Cluster()
    cluster.add_node(node)
    assert cluster.nodes == [node]

def test_remove_node_from_cluster():
    node_1 = Node(url="test.node_1.com")
    node_2 = Node(url="test.node_2.com")
    cluster = Cluster(nodes=[node_1, node_2])
    cluster.remove_node(node_1)
    assert cluster.nodes == [node_2]

def test_add_group_to_cluster_with_one_node():
    cluster = Cluster()
    cluster.add_node(Node(url="test.node_1.com"))

    test_group_1 = Group(groupID="group_1")
    cluster.add_group(test_group_1)

    assert test_group_1 in cluster.nodes[0].groups

def test_add_group_to_cluster_with_multiple_nodes():
    cluster = Cluster()
    cluster.add_node(Node(url="test.node_1.com"))
    cluster.add_node(Node(url="test.node_2.com"))

    test_group_1 = Group(groupID="group_1")
    cluster.add_group(test_group_1)

    assert test_group_1 in cluster.nodes[0].groups
    assert test_group_1 in cluster.nodes[1].groups

def test_remove_group_from_cluster_with_one_node():
    test_group_1 = Group(groupID="group_1")

    cluster = Cluster(nodes=[Node(url="test.node_1.com", groups=[test_group_1])])
    cluster.remove_group(test_group_1)

    assert test_group_1 not in cluster.nodes[0].groups
    
def test_remove_group_from_cluster_with_multiple_nodes():
    test_group_1 = Group(groupID="group_1")

    cluster = Cluster(nodes=[
        Node(url="test.node_1.com", groups=[test_group_1]),
        Node(url="test.node_2.com", groups=[test_group_1])
    ])
    cluster.remove_group(test_group_1)

    assert test_group_1 not in cluster.nodes[0].groups
    assert test_group_1 not in cluster.nodes[1].groups

def test_remove_group_from_inconsistent_cluster():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")

    cluster = Cluster(nodes=[
        Node(url="test.node_1.com", groups=[test_group_1]),
        Node(url="test.node_2.com", groups=[test_group_1, test_group_2])
    ])

    with pytest.raises(Exception):
        cluster.remove_group(test_group_2)

def test_validate_cluster_consistency_on_consistent_cluster():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")

    cluster = Cluster(nodes=[
        Node(url="test.node_1.com", groups=[test_group_1, test_group_2]),
        Node(url="test.node_2.com", groups=[test_group_1, test_group_2])
    ])

    assert cluster.validate_consistency() == True
    
def test_validate_cluster_consistency_on_inconsistent_cluster():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")

    cluster = Cluster(nodes=[
        Node(url="test.node_1.com", groups=[test_group_1, test_group_2]),
        Node(url="test.node_2.com", groups=[test_group_1])
    ])

    assert cluster.validate_consistency() == False

def test_rollback_cluster():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    test_group_3 = Group(groupID="group_3")
    test_group_4 = Group(groupID="group_4")

    cluster = Cluster(nodes=[
        Node(url="test.node_1.com", groups=[test_group_1, test_group_2]),
        Node(url="test.node_2.com", groups=[test_group_1, test_group_2, test_group_3]),
        Node(url="test.node_3.com", groups=[test_group_1, test_group_2, test_group_3])
    ])

    cluster.rollback()

    assert cluster.nodes[0].groups == [test_group_1, test_group_2]
    assert cluster.nodes[1].groups == [test_group_1, test_group_2]
    assert cluster.nodes[2].groups == [test_group_1, test_group_2]

def test_find_existing_group():
    test_group_1 = Group(groupID="group_1")
    test_group_2 = Group(groupID="group_2")
    test_group_3 = Group(groupID="group_3")

    cluster = Cluster(nodes=[
        Node(url="test.node_1.com", groups=[test_group_1, test_group_2, test_group_3]),
        Node(url="test.node_2.com", groups=[test_group_1, test_group_2, test_group_3]),
        Node(url="test.node_3.com", groups=[test_group_1, test_group_2, test_group_3])
    ])

    assert find_group(cluster, 'group_3') == test_group_3