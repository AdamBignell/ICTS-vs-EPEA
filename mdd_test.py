import mdd
import map_utils as util

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
    depth = 3
    new_mdd = mdd.MDD(my_map, 0, starts[agent], goals[agent], depth)
    bfs_tree = new_mdd.get_depth_d_bfs_tree(my_map, starts[agent], goals[agent], depth)
    for node in bfs_tree.keys():
        for val in bfs_tree[node]:
            loc, t = val
            assert not my_map[loc[0]][loc[1]], "test_depth_d_bfs_tree Failed: BFS explores invalid cells"
            assert t <= depth, "test_depth_d_bfs_tree Failed: BFS explores to depth greater than " + str(depth)
    print("test_depth_d_bfs_tree Passed")

def test_mdd_generation(my_map, starts, goals):
    agent = 0
    depth = 4
    new_mdd = mdd.MDD(my_map, 0, starts[agent], goals[agent], depth)
    # Hardcoded test for a simple case below
    assert new_mdd.mdd[((1, 1), 0)] == [((2, 1), 1), ((1, 2), 1)], "test_mdd_generation Failed: test case ((1, 1), 0) -> ((2, 1), 1), ((1, 2), 1) failed"
    assert new_mdd.mdd[((1, 2), 1)] == [((2, 2), 2), ((1, 3), 2)], "test_mdd_generation Failed: test case ((1, 2), 1) -> ((2, 2), 2), ((1, 3), 2) failed"
    assert new_mdd.mdd[((2, 1), 1)] == [((2, 2), 2)], "test_mdd_generation Failed: test case ((2, 1), 1) -> ((2, 2), 2) failed"
    assert new_mdd.mdd[((1, 3), 2)] == [((2, 3), 3)], "test_mdd_generation Failed: test case (((1, 3), 2) -> ((2, 3), 3) failed"
    assert new_mdd.mdd[((2, 2), 2)] == [((3, 2), 3), ((2, 3), 3)], "test_mdd_generation Failed: test case ((2, 2), 2) -> ((3, 2), 3), ((2, 3), 3) failed"
    assert new_mdd.mdd[((2, 3), 3)] == [((3, 3), 4)], "test_mdd_generation Failed: test case ((2,3),3) -> ((3,3),4) failed"
    assert new_mdd.mdd[((3, 2), 3)] == [((3, 3), 4)], "test_mdd_generation Failed: test case ((3,2),3) -> ((3,3),4) failed"
    print("test_mdd_generation Passed")

def test_mdd_level_i(my_map, starts, goals):
    agent = 0
    depth = 4
    new_mdd = mdd.MDD(my_map, agent, starts[agent], goals[agent], depth)
    assert [starts[agent]] == new_mdd.get_level(0), "test_mdd_level_i Failed: Level 0 isn't the start node"
    assert [(2, 1), (1, 2)] == new_mdd.get_level(1), "test_mdd_level_i Failed: Level 1 isn't [((2, 1), 1), ((1, 2), 1)]"
    print("test_mdd_level_i Passed")

def test_joint_mdd_search(my_map, starts, goals):
    a1 = 0
    a2 = 1
    depth = 2 # No solution
    a1_mdd = mdd.MDD(my_map, a1, starts[a1], goals[a1], depth)
    a2_mdd = mdd.MDD(my_map, a2, starts[a2], goals[a2], depth)
    solution = mdd.is_solution_in_joint_mdd([a1_mdd, a2_mdd])
    assert solution == False, "test_joint_mdd_search Failed: Finds a solution when none exists"

    depth = 3 # Solution
    a1_mdd = mdd.MDD(my_map, a1, starts[a1], goals[a1], depth)
    a2_mdd = mdd.MDD(my_map, a2, starts[a2], goals[a2], depth)
    solution = mdd.is_solution_in_joint_mdd([a1_mdd, a2_mdd])
    assert solution == True, "test_joint_mdd_search Failed: Finds no solution when one exists"
    print("test_joint_mdd_search Passed")

if __name__ == '__main__':
    my_map, starts, goals = util.import_mapf_instance("instances/mdd_test.txt")
    print(" === Running MDD Tests === ")
    test_simple_construction(my_map, starts, goals)
    test_depth_d_bfs_tree(my_map, starts, goals)
    test_mdd_generation(my_map, starts, goals)
    test_mdd_level_i(my_map, starts, goals)

    my_joint_map, starts, goals = util.import_mapf_instance("instances/joint_mdd_test.txt")
    test_joint_mdd_search(my_joint_map, starts, goals)