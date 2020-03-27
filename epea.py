import time as timer
from heapq import heappush
from heapq import heappop
import random
from osf import OSF
import math
from single_agent_planner import compute_heuristics, a_star, get_location, get_sum_of_cost

class EPEASolver(object):
    """A high-level EPEA* search."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.num_of_generated = 0
        self.num_of_expanded = 0
        self.CPU_time = 0

        self.open_list = []
        self.visited = []

        self.osf = OSF(my_map, goals)

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations
        """
        print("\nFinding EPEA* Solution...")
        return self.epea_star()

    
    def epea_star(self):
        osf = self.osf
        open_list = self.open_list
        start_locs = self.starts
        goals = self.goals
        visited = self.visited
        num_agents = len(start_locs)

        g = 0
        h = osf.list_of_locations_to_heuristic(start_locs)

        #for agent, loc in enumerate(starts):
        #    h += osf.h[agent][starts[agent][0]][starts[agent][1]]

        start_node = {'agent_locs': start_locs, 'g': 0, 'h': h, 'small_f': g + h, 'big_F': g + h, 'parent': False}
        heappush(open_list, start_node)
        while(len(open_list) != 0):
            current_node = heappop(open_list)
            if current_node['agent_locs'] == goals:
                return self.find_paths(current_node)        # to be implemented: returning path etc.
            new_child_nodes, next_big_F = osf.get_children_and_next_F(current_node['agent_locs'], current_node['big_F'], current_node['h'], current_node['g'])

            for child in new_child_nodes:
                if any(child in node.values() for node in open_list):
                    continue
                h = osf.list_of_locations_to_heuristic(child)
                g = current_node['g'] + num_agents
                small_f = g + h
                big_F = small_f
                new_node = {'agent_locs': child, 'g': g, 'h': h, 'small_f': small_f, 'big_F': big_F}
                heappush(open_list, new_node)
            
            if math.isinf(next_big_F):
                heappush(visited, current_node)
            else:
                current_node['big_F'] = next_big_F
                heappush(open_list, current_node)
            return None
        
    def find_paths(self, node):
        return "success"
