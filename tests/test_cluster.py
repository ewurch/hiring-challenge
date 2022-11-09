from cluster.core import Group

def test_get_group():
    group = Group(groupID="test")
    assert group.groupID == "test"