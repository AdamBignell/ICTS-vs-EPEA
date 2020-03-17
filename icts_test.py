import map_utils

from ict import IncreasingCostTree
from icts import ICTSSolver

def test_find_most_optimal_paths():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    optimal_paths = icts.find_most_optimal_paths()
    assert optimal_paths == [[(1,1), (1,2), (1,3), (1,4), (1,5)], [(1,2), (1,3), (1,4)]], "Cannot find most optimal paths of a map instance"

def test_find_most_optimal_cost_of_paths():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    cost_of_optimal_paths = icts.find_cost_of_initial_estimate_for_root()
    assert cost_of_optimal_paths == [4, 2], "Cannot find cost of most optimal paths of a map instance"

def test_create_initial_cost_for_ict():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    root = icts.ict.get_next_node_to_expand()
    root_costs = root.get_cost()
    assert root_costs == [4, 2], "Cost of the root node of the ict is incorrect"

def test_bfs_on_ict_with_valid_solution():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    icts = ICTSSolver(my_map, starts, goals)
    solution = icts.find_solution()
    assert solution == [[(1,1), (1,2), (1,3), (1,4), (1,5)],
                        [(1,2), (1,3), (2,3), (1,3), (1,4)]], "BFS in ICTS could not find solution even though valid solution exists"

if __name__ == "__main__":
    test_find_most_optimal_paths()
    test_find_most_optimal_cost_of_paths()
    test_create_initial_cost_for_ict()
    test_bfs_on_ict_with_valid_solution()
    print("ALL TEST PASSED")