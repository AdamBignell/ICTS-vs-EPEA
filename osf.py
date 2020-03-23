# Operator Selection Function for MAPF
# Used in EPEA*
from collections import deque
from collections import defaultdict
import itertools
import time
import math

class OSF:
    def __init__(self, my_map, goals):
        """OSF is a singleton that calculates the next operator for any given step."""
        self.map = my_map

        # usage: h[agent][x][y]
        self.h = self.get_heuristics(self.map, goals)
        self.visited = set()
        self.indiv_ops = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
        self.osf_tables = dict()

    def get_heuristics(self, my_map, goals):
        num_agents = len(goals)
        all_h = []
        for i in range(num_agents):
            this_goal = goals[i]
            new_h = []
            for x, row in enumerate(my_map):
                this_row_h = []
                for y, cell in enumerate(row):
                    if cell:
                        this_row_h.append(math.inf)
                    else:
                        this_row_h.append(self.manhattan_distance((x,y), this_goal))
                new_h.append(this_row_h)
            all_h.append(new_h)
        return all_h

    def manhattan_distance(self, loc1, loc2):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])
        
    def select_operator(self, agent_locs, big_F, h, g):
        op_table = dict()
        small_f = h + g
        ops_to_cross_prod = [self.indiv_ops for i in range(agent_locs)]
        all_possible_ops = list(itertools.product(*ops_to_cross_prod))
        delta_big_F = math.inf
        requested_row = big_F - small_f
        for op in all_possible_ops:
            new_op_table_row = dict()
            this_h = self.compute_group_heuristic(op, agent_locs)
            this_g = g + 1
            this_small_f = this_h + this_g
            delta_small_f = this_small_f - small_f
            if delta_small_f not in op_table:
                new_op_table_row['delta_h'] = this_h - h
                new_op_table_row['operators'] = [op]
                op_table[this_small_f] = new_op_table_row
            else:
                op_table[this_small_f]['operators'].append(op)
            if delta_small_f > requested_row and delta_small_f < delta_big_F:
                delta_big_F = delta_small_f
        return op_table[requested_row]['operators'], delta_big_F
        

    def compute_group_heuristic(self, ops, locs):
        h = 0
        for i, op in enumerate(ops):
            new_x = locs[i][0] + op[0]
            new_y = locs[i][1] + op[1]
            h += self.h[i][new_x][new_y]
        return h