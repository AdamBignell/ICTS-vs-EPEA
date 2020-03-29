#!/usr/bin/python
import argparse
import glob
from icts import ICTSSolver
from epea import EPEASolver
from visualize import Animation
from single_agent_planner import get_sum_of_cost
import map_utils as util
import time

SOLVER = "ICTS"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compares ICTS and EPEA* Algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    parser.add_argument('--batch', action='store_true', default=False,
                        help='Use batch output instead of animation')
    parser.add_argument('--solver', type=str, default=SOLVER,
                        help='The solver to use (one of: {ICTS,EPEA}), defaults to ' + str(SOLVER))

    args = parser.parse_args()

    for file in sorted(glob.glob(args.instance)):

        print("***Import an instance***")
        my_map, starts, goals = util.import_mapf_instance(file)
        util.print_mapf_instance(my_map, starts, goals)
        
        paths = []
        if args.solver == "ICTS":
            print("***Run ICTS***")
            icts = ICTSSolver(my_map, starts, goals)
            if not icts.ict:
                paths = []
            else:
                t1 = time.time()
                paths = icts.find_solution()
                t2 = time.time()
                print("Found solution in this many seconds = ", t2-t1)
        elif args.solver == "EPEA":
            print("***Run EPEA***")
            epea = EPEASolver(my_map, starts, goals)
            t1 = time.time()
            paths = epea.find_solution()
            t2 = time.time()
            print("Found solution in this many seconds = ", t2-t1)
        else:
            raise RuntimeError("Unknown solver!")

        if not paths:
            raise RuntimeError("No Solution!")

        cost = get_sum_of_cost(paths)
        result_file = open("results_" + "args.solver" + ".csv", "w", buffering=1)
        result_file.write("{},{}\n".format(file, cost))

        if not args.batch:
            print("***Test paths on a simulation***")
            animation = Animation(my_map, starts, goals, paths)
            # animation.save("output.mp4", 1.0)
            animation.show()

    result_file.close()
