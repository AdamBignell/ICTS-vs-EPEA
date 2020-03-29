import osf
import map_utils as util
import math

def test_simple_osf_construction(my_map, goals):
    new_osf = osf.OSF(my_map, goals)
    print("Printing heuristics for reference...")
    new_osf.print_heuristics()
    assert new_osf.h, "test_simple_construction Failed: Heuristics not set"
    assert new_osf.indiv_ops == [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)], "test_simple_construction Failed: Operators not set"
    print("test_simple_osf_construction Passed")

def test_operator_selection(my_map, starts, goals):
    new_osf = osf.OSF(my_map, goals)
    agent_locs = starts
    h = new_osf.list_of_locations_to_heuristic(agent_locs)
    g = 0
    big_F = h + g
    node = {'agent_locs': agent_locs, 'g': g, 'h': h, 'small_f': g + h, 'big_F': big_F, 'parent': False}
    operators, next_big_F = new_osf.select_operators(node)
    correct_operators = [((1, 0), (-1, 0)), ((1, 0), (0, 1)), ((0, 1), (-1, 0)), ((0, 1), (0, 1))]
    assert operators == correct_operators, "test_operator_selection Failed: Incorrect operators returned"
    assert next_big_F == 7, "test_operator_selection Failed: Next big F value incorrect"
    print("test_operator_selection Passed")

def test_new_children(my_map, starts, goals):
    new_osf = osf.OSF(my_map, goals)
    agent_locs = starts
    h = new_osf.list_of_locations_to_heuristic(agent_locs)
    g = 0
    big_F = h + g
    node = {'agent_locs': agent_locs, 'g': g, 'h': h, 'small_f': g + h, 'big_F': big_F, 'parent': False}
    children, next_big_F = new_osf.get_children_and_next_F(node)
    assert children == [((2, 1), (2, 2)), ((2, 1), (3, 3)), ((1, 2), (2, 2)), ((1, 2), (3, 3))], "test_new_children Failed: Incorrect children returned"
    assert next_big_F == 7, "test_new_children Failed: Incorrect next_F returned"
    print("test_new_children Passed")

def test_three_agent_around(my_map, starts, goals):
    new_osf = osf.OSF(my_map, goals)
    agent_locs = starts
    h = new_osf.list_of_locations_to_heuristic(agent_locs)
    g = 0
    big_F = h + g
    node = {'agent_locs': agent_locs, 'g': g, 'h': h, 'small_f': g + h, 'big_F': big_F, 'parent': False}
    children, next_big_F = new_osf.get_children_and_next_F(node)
    assert not children, "test_three_agent_around Failed: Children found when no possible operators should allow for the requested big_F"
    big_F = h + g + 2 # Since two agents do not get closer to their goals, and one does
    node['big_F'] = big_F
    children, next_big_F = new_osf.get_children_and_next_F(node)
    assert children == [((2, 1), (3, 5), (1, 7)), ((1, 2), (3, 5), (1, 7))], "test_three_agent_around Failed: Children do not properly circumvent obstacles"
    print("test_new_children Passed")

if __name__ == '__main__':
    print(" === Running OSF Tests === ")
    my_map, starts, goals = util.import_mapf_instance("instances/osf_test.txt")
    test_simple_osf_construction(my_map, goals)
    test_operator_selection(my_map, starts, goals)
    test_new_children(my_map, starts, goals)

    my_map, starts, goals = util.import_mapf_instance("instances/osf_3_agent_around_test.txt")
    test_three_agent_around(my_map, starts, goals)
    print("All Tests Passed!")