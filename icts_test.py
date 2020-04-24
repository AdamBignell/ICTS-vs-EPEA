import map_utils
from map_utils import MapDetails
from ict import IncreasingCostTree, TreeNode
from icts import ICTSSolver

file_name = "instances/exp2_1.txt"
my_map, starts, goals = map_utils.import_mapf_instance(file_name)
map_details1 = MapDetails("results/icts_test.txt", file_name, my_map, starts, goals)

no_solutions = "instances/no_solution.txt"
my_map, starts, goals = map_utils.import_mapf_instance(no_solutions)
map_details2 = MapDetails("results/icts_test.txt", no_solutions, my_map, starts, goals)

def test_find_most_optimal_paths():
    icts = ICTSSolver(map_details1)
    optimal_paths = icts.find_most_optimal_paths()
    assert optimal_paths == [[(1,1), (1,2), (1,3), (1,4), (1,5)], [(1,2), (1,3), (1,4)]], "Cannot find most optimal paths of a map instance"

def test_find_most_optimal_cost_of_paths():
    icts = ICTSSolver(map_details1)
    cost_of_optimal_paths = icts.find_cost_of_initial_estimate_for_root()
    assert cost_of_optimal_paths == [4, 2], "Cannot find cost of most optimal paths of a map instance"

def test_create_initial_cost_for_ict():
    icts = ICTSSolver(map_details1)
    root = icts.ict.get_next_node_to_expand()
    root_costs = root.get_cost()
    assert root_costs == [4, 2], "Cost of the root node of the ict is incorrect"

def test_bfs_on_ict_with_valid_solution():
    icts = ICTSSolver(map_details1)
    solution = icts.find_solution()
    assert solution == [[(1,1), (1,2), (1,3), (1,4), (1,5)],
                        [(1,2), (1,3), (2,3), (1,3), (1,4)]], "BFS in ICTS could not find solution even though valid solution exists"
    print("Found solution.")

def test_number_of_open_spaces():
    number_of_open_spaces = map_utils.find_number_of_open_spaces(map_details2.map_instance)
    assert number_of_open_spaces == 5, "ICTS cannot find the correct number of open spaces in a map"

def test_calculate_upperbound_cost_of_all_agents():
    icts = ICTSSolver(map_details2)
    upper_bound = icts.calculate_upper_bound_cost()
    assert upper_bound == 20, "ICTS cannot find the correct upper bound for a map"

def test_node_has_exceeded_upper_bound():
    node = TreeNode([10, 11])
    upper_bound = 20

    icts = ICTSSolver(map_details2)
    node_exceeds_bound = icts.node_has_exceeded_upper_bound(node, upper_bound)

    assert node_exceeds_bound is True, "ICTS believes nodes has not exceeded the upper bound even though the node exceeds the upper bound"

def test_node_has_not_exceeded_upper_bound():
    node = TreeNode([10, 9])
    upper_bound = 20

    icts = ICTSSolver(map_details2)
    node_exceeds_bound = icts.node_has_exceeded_upper_bound(node, upper_bound)

    assert node_exceeds_bound is False, "ICTS believes nodes has exceeded the upper bound even though the node has not exceeded the upper bound"

def test_bfs_terminates_if_no_solution_exists():
    icts = ICTSSolver(map_details2)
    solution_paths = icts.find_solution()
    assert solution_paths == [], "ICTS returns a solution when no solution exists"
    print("Could not find solution.")

if __name__ == "__main__":
    test_find_most_optimal_paths()
    test_find_most_optimal_cost_of_paths()
    test_create_initial_cost_for_ict()
    test_bfs_on_ict_with_valid_solution()
    test_number_of_open_spaces()
    test_calculate_upperbound_cost_of_all_agents()
    test_node_has_exceeded_upper_bound()
    test_node_has_not_exceeded_upper_bound()
    test_bfs_terminates_if_no_solution_exists()
    print("ALL TEST PASSED")