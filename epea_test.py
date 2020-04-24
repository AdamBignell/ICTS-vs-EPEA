import epea
import map_utils
from map_utils import MapDetails

output_file_name = 'results/epea_test_output'

def test_epea_with_valid_solution():
    file_name = "instances/exp2_1.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    map_details = MapDetails(output_file_name, file_name, my_map, starts, goals)
    epea_sol = epea.EPEASolver(map_details)
    solution = epea_sol.find_solution()
    assert solution == [[(1,1), (1,2), (1,3), (1,4), (1,5)],
                        [(1,2), (1,3), (2,3), (1,3), (1,4)]], "EPEA* could not find solution even though valid solution exists"
    print("Found solution.")

def test_epea_with_valid_solution2():
    file_name = "instances/exp2_2.txt"
    my_map, starts, goals = map_utils.import_mapf_instance(file_name)
    map_details = MapDetails(output_file_name, file_name, my_map, starts, goals)
    epea_sol = epea.EPEASolver(map_details)
    solution = epea_sol.find_solution()
    assert solution == [[(1,2), (1,3), (1,4), (2,4), (1,4)],
                        [(1,1), (1,2), (1,3), (1,4), (1,5)]], "EPEA* could not find solution even though valid solution exists"

if __name__ == '__main__':
    print(" === Running epea* Tests === ")
    test_epea_with_valid_solution2()
    print("ALL TEST PASSED")