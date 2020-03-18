from ict import IncreasingCostTree, TreeNode

def test_constructor_adds_root_to_open_list():
    ict = IncreasingCostTree([], [], [], (10, 10, 10))
    open_list = ict.get_open_list()
    root = open_list.pop(0)
    assert root is not None, "Cannot construct ict"

def test_getting_node_to_expand():
    ict = IncreasingCostTree([], [], [], (10, 10, 10))
    next_node = ict.get_next_node_to_expand()
    assert next_node is not None, "Cannot get next node for expansion"

def test_create_correct_number_of_children():
    ict = IncreasingCostTree([], [], [], (10, ))
    next_node = ict.get_next_node_to_expand()
    next_node.expand_node()
    number_of_children = len(next_node.get_all_children())
    assert number_of_children == 1, "Number of children after expansion is incorrect"

def test_creating_correct_cost_of_single_child():
    ict = IncreasingCostTree([], [], [], (10, ))
    next_node = ict.get_next_node_to_expand()
    next_node.expand_node()
    first_child = next_node.get_ith_child(0)
    child_cost = first_child.get_cost()
    assert child_cost == (11, ), "Path cost of newly expanded node is incorrect"

def test_creating_correct_cost_of_multiple_children():
    ict = IncreasingCostTree([], [], [], (10, 10, 10))
    next_node = ict.get_next_node_to_expand()
    next_node.expand_node()
    first_child = next_node.get_ith_child(0)
    second_child = next_node.get_ith_child(1)
    third_child = next_node.get_ith_child(2)
    assert first_child.get_cost() == (11, 10, 10) and \
        second_child.get_cost() == (10, 11, 10) and \
        third_child.get_cost() == (10, 10, 11), "Path cost of newly expanded node with multiple children is incorrect"

def test_child_nodes_are_added_to_open_list():
    ict = IncreasingCostTree([], [], [], (10, 10, 10))
    ict.expand_next_node()
    ict.pop_next_node_to_expand()
    open_list = ict.get_open_list()
    assert len(open_list) == 3, "Child nodes not correctly added to open list of ict"

def test_expanding_node_from_tree():
    ict = IncreasingCostTree([], [], [], (10, 10, 10))
    ict.expand_next_node()
    ict.pop_next_node_to_expand()
    next_node = ict.get_next_node_to_expand()
    node_cost = next_node.get_cost()
    assert node_cost == (11, 10, 10), "Path cost of newly expanded node from ict with multiple children is incorrect"

def test_duplicate_node_is_not_added_to_open_list():
    ict = IncreasingCostTree([], [], [], (10, 10, 10))
    future_node = TreeNode((11, 10, 10))
    ict.add_unexplored_node_to_open_list(future_node)
    ict.expand_next_node()
    ict.pop_next_node_to_expand()

    open_list = ict.get_open_list()
    assert open_list[0].get_cost() == (11, 10, 10) and \
           open_list[1].get_cost() == (10, 11, 10) and \
           open_list[2].get_cost() == (10, 10, 11), "Duplicate node was added to the open list when it shouldn't have been"

if __name__ == "__main__":
    test_constructor_adds_root_to_open_list()
    test_getting_node_to_expand()
    test_create_correct_number_of_children()
    test_creating_correct_cost_of_single_child()
    test_creating_correct_cost_of_multiple_children()
    test_child_nodes_are_added_to_open_list()
    test_expanding_node_from_tree()
    test_duplicate_node_is_not_added_to_open_list()
    print("ALL TEST PASSED")