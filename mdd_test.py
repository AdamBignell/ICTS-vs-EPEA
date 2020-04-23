import mdd
import map_utils as util
from performance_tracker import PerformanceTracker

dummy_tracker = PerformanceTracker("test")

def test_simple_construction(my_map, starts, goals):
    agent = 0
    depth = 7 # Arbitrary depth
    new_mdd = mdd.MDD(my_map, 0, starts[agent], goals[agent], depth, False)
    assert new_mdd.agent == 0, "test_simple_construction Failed: Agent is improperly set"
    assert new_mdd.depth == depth, "test_simple_construction Failed: Depth is improperly set"
    assert new_mdd.start == starts[agent], "test_simple_construction Failed: Start is improperly set"
    assert new_mdd.goal == goals[agent], "test_simple_construction Failed: Goal is improperly set"
    print("test_simple_construction Passed")

def test_depth_d_bfs_tree(my_map, starts, goals):
    agent = 0
    depth = 4
    new_mdd = mdd.MDD(my_map, 0, starts[agent], goals[agent], depth)
    bfs_tree_dict = new_mdd.get_depth_d_bfs_tree(my_map, starts[agent], depth)
    bfs_tree = bfs_tree_dict['tree']
    for node in bfs_tree.keys():
        for val in bfs_tree[node]:
            loc, t = val
            assert not my_map[loc[0]][loc[1]], "test_depth_d_bfs_tree Failed: BFS explores invalid cells"
            assert t <= depth, "test_depth_d_bfs_tree Failed: BFS explores to depth greater than " + str(depth)
    print("test_depth_d_bfs_tree Passed")

def test_bootstrap_bfs_tree(my_map, starts, goals):
    agent = 0
    depth = 4
    mdd_4 = mdd.MDD(my_map, 0, starts[agent], goals[agent], depth)
    mdd_5 = mdd.MDD(my_map, 0, starts[agent], goals[agent], depth+1, mdd_4)
    bfs_tree = mdd_5.bfs_tree['tree']
    for node in bfs_tree.keys():
        for val in bfs_tree[node]:
            loc, t = val
            assert not my_map[loc[0]][loc[1]], "test_bootstrap_bfs_tree Failed: Bootstrap BFS explores invalid cells"
            assert t <= depth+1, "test_bootstrap_bfs_tree Failed: Bootstrap BFS explores to depth greater than " + str(depth+1)
    print("test_bootstrap_bfs_tree Passed")   

def test_mdd_generation(my_map, starts, goals):
    agent = 0
    depth = 4
    new_mdd = mdd.MDD(my_map, 0, starts[agent], goals[agent], depth)
    # Hardcoded test for a simple case below
    assert set(new_mdd.mdd[((1, 1), 0)]) == set([((2, 1), 1), ((1, 2), 1)]), "test_mdd_generation Failed: test case ((1, 1), 0) -> ((2, 1), 1), ((1, 2), 1) failed"
    assert set(new_mdd.mdd[((1, 2), 1)]) == set([((2, 2), 2), ((1, 3), 2)]), "test_mdd_generation Failed: test case ((1, 2), 1) -> ((2, 2), 2), ((1, 3), 2) failed"
    assert set(new_mdd.mdd[((2, 1), 1)]) == set([((2, 2), 2)]), "test_mdd_generation Failed: test case ((2, 1), 1) -> ((2, 2), 2) failed"
    assert set(new_mdd.mdd[((1, 3), 2)]) == set([((2, 3), 3)]), "test_mdd_generation Failed: test case (((1, 3), 2) -> ((2, 3), 3) failed"
    assert set(new_mdd.mdd[((2, 2), 2)]) == set([((3, 2), 3), ((2, 3), 3)]), "test_mdd_generation Failed: test case ((2, 2), 2) -> ((3, 2), 3), ((2, 3), 3) failed"
    assert set(new_mdd.mdd[((2, 3), 3)]) == set([((3, 3), 4)]), "test_mdd_generation Failed: test case ((2,3),3) -> ((3,3),4) failed"
    assert set(new_mdd.mdd[((3, 2), 3)]) == set([((3, 3), 4)]), "test_mdd_generation Failed: test case ((3,2),3) -> ((3,3),4) failed"
    print("test_mdd_generation Passed")

def test_mdd_level_i(my_map, starts, goals):
    agent = 0
    depth = 4
    new_mdd = mdd.MDD(my_map, agent, starts[agent], goals[agent], depth)
    assert {starts[agent]} == new_mdd.get_level(0), "test_mdd_level_i Failed: Level 0 isn't the start node"
    assert set([(2, 1), (1, 2)]) == set(new_mdd.get_level(1)), "test_mdd_level_i Failed: Level 1 isn't [((2, 1), 1), ((1, 2), 1)]"
    print("test_mdd_level_i Passed")

def test_two_agent_joint_mdd_search(my_map, starts, goals):
    a1, a2 = 0, 1
    depth = 2 # No solution
    a1_mdd = mdd.MDD(my_map, a1, starts[a1], goals[a1], depth)
    a2_mdd = mdd.MDD(my_map, a2, starts[a2], goals[a2], depth)
    found_path = mdd.is_solution_in_joint_mdd([a1_mdd, a2_mdd], dummy_tracker)
    assert found_path == False, "test_two_agent_joint_mdd_search Failed: Finds a solution when none exists"

    depth = 3 # Solution
    a1_mdd = mdd.MDD(my_map, a1, starts[a1], goals[a1], depth)
    a2_mdd = mdd.MDD(my_map, a2, starts[a2], goals[a2], depth)
    found_path = mdd.is_solution_in_joint_mdd([a1_mdd, a2_mdd], dummy_tracker)
    assert found_path == True, "test_two_agent_joint_mdd_search Failed: Finds no solution when one exists"

    depth1 = 3
    depth2 = 2 # Mismatched solution depths
    a1_mdd = mdd.MDD(my_map, a1, starts[a1], goals[a1], depth1)
    a2_mdd = mdd.MDD(my_map, a2, starts[a2], goals[a2], depth2)  
    found_path = mdd.is_solution_in_joint_mdd([a1_mdd, a2_mdd], dummy_tracker)
    assert found_path == True, "test_two_agent_joint_mdd_search Failed: Finds no solution when the depth of the input mdds mismatch"

def test_three_agent_joint_mdd_search(my_map, starts, goals):
    depth = 4
    a1, a2, a3 = 0, 1, 2
    a1_mdd = mdd.MDD(my_map, a1, starts[a1], goals[a1], depth)
    a2_mdd = mdd.MDD(my_map, a2, starts[a2], goals[a2], depth) 
    a3_mdd = mdd.MDD(my_map, a3, starts[a3], goals[a3], depth)
    found_path = mdd.is_solution_in_joint_mdd([a1_mdd, a2_mdd, a3_mdd], dummy_tracker)
    assert found_path == True, "test_three_agent_joint_mdd_search Failed: Finds no solution with 3 agents when one exists"
    print("test_three_agent_joint_mdd_search Passed")

def test_find_solution_in_joint_mdd(my_map, starts, goals):
    depth = 4
    a1, a2, a3 = 0, 1, 2
    a1_mdd = mdd.MDD(my_map, a1, starts[a1], goals[a1], depth)
    a2_mdd = mdd.MDD(my_map, a2, starts[a2], goals[a2], depth) 
    a3_mdd = mdd.MDD(my_map, a3, starts[a3], goals[a3], depth)
    solution_path = mdd.find_solution_in_joint_mdd([a1_mdd, a2_mdd, a3_mdd], dummy_tracker)
    for i in range(len(solution_path[0])-1):
        this_locs = [solution_path[j][i] for j in range(len(solution_path))]
        next_locs = [solution_path[j][i+1] for j in range(len(solution_path))]
        assert all_moves_valid(this_locs, next_locs), "test_find_solution_in_joint_mdd Failed: Finds a solution with invalid steps"
    print("test_find_solution_in_joint_mdd Passed")

def test_find_no_solution_where_none_exists(my_map, starts, goals):
    depth = 5
    a1, a2 = 0, 1
    a1_mdd = mdd.MDD(my_map, a1, starts[a1], goals[a1], depth)
    a2_mdd = mdd.MDD(my_map, a2, starts[a2], goals[a2], depth)  
    solution_path = mdd.find_solution_in_joint_mdd([a1_mdd, a2_mdd], dummy_tracker)
    assert solution_path == None, "test_find_no_solution_where_none_exists Failed: Finds a solution where none exists"
    print("test_find_no_solution_where_none_exists Passed")

def all_moves_valid(this_locs, next_locs):
    forward = [pair for pair in zip(this_locs, next_locs)]
    has_edge_collision = mdd.has_edge_collisions(this_locs, next_locs)
    for pair in forward:
        this_loc = pair[0]
        next_loc = pair[1]
        if sum([abs(this_loc[0] - next_loc[0]), abs(this_loc[1] - next_loc[1])]) > 1:
            return False
    return not has_edge_collision

if __name__ == '__main__':
    my_map, starts, goals = util.import_mapf_instance("instances/mdd_test.txt")
    print(" === Running MDD Tests === ")
    test_simple_construction(my_map, starts, goals)
    test_depth_d_bfs_tree(my_map, starts, goals)
    test_bootstrap_bfs_tree(my_map, starts, goals)
    test_mdd_generation(my_map, starts, goals)
    test_mdd_level_i(my_map, starts, goals)

    my_joint_map, starts, goals = util.import_mapf_instance("instances/joint_mdd_test.txt")
    test_two_agent_joint_mdd_search(my_joint_map, starts, goals)

    my_3_agent_joint_map, starts, goals = util.import_mapf_instance("instances/joint_mdd_3_agent_test.txt")
    test_three_agent_joint_mdd_search(my_3_agent_joint_map, starts, goals)
    test_find_solution_in_joint_mdd(my_3_agent_joint_map, starts, goals)

    my_impossible_map, starts, goals = util.import_mapf_instance("instances/no_solution.txt")
    test_find_no_solution_where_none_exists(my_impossible_map, starts, goals)
