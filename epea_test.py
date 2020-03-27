import epea
import map_utils
import math

def test_epea_with_valid_solution():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    epea_sol = epea.EPEASolver(my_map, starts, goals)
    solution = epea_sol.find_solution()
    assert solution == [[(1,1), (1,2), (1,3), (1,4), (1,5)],
                        [(1,2), (1,3), (2,3), (1,3), (1,4)]], "EPEA* could not find solution even though valid solution exists"
    print("Found solution.")

def test_epea_with_valid_solution2():
    file_name = "instances/exp2_2.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    epea_sol = epea.EPEASolver(my_map, starts, goals)
    solution = epea_sol.find_solution()
    assert solution == [[(1,2), (1,3), (2,3), (1,3), (1,4)],
                        [(1,1), (1,2), (1,3), (1,4), (1,5)]], "EPEA* could not find solution even though valid solution exists"

if __name__ == '__main__':
    print(" === Running epea* Tests === ")
    test_epea_with_valid_solution2()
    print("ALL TEST PASSED")