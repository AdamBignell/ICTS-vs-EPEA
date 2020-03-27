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
        self.visited = set()

        self.osf = OSF(my_map, goals)

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations
        """
        print("\nFinding EPEA* Solution...")
        return self.epea_star()

    
    def epea_star(self):
        osf = self.osf
        open_list = self.open_list
        start_locs = tuple(self.starts)
        goals = self.goals
        visited = self.visited
        num_agents = len(start_locs)
        mycounter = 0       # counter that is used to break ties in the priority queue
        g = 0
        h = osf.list_of_locations_to_heuristic(start_locs)

        #for agent, loc in enumerate(starts):
        #    h += osf.h[agent][starts[agent][0]][starts[agent][1]]

        start_node = {'agent_locs': start_locs, 'g': 0, 'h': h, 'small_f': g + h, 'big_F': g + h, 'parent': False}
        heappush(open_list, (start_node['big_F'], mycounter, start_node))
        mycounter+=1
        while(len(open_list) != 0):
            priority, count, current_node = heappop(open_list)
            if current_node['agent_locs'] == goals:
                return self.find_paths(current_node)
            print("calling OSF with:", current_node['agent_locs'], current_node['big_F'], current_node['h'], current_node['g'])
            new_child_nodes, next_big_F = osf.get_children_and_next_F(current_node['agent_locs'], current_node['big_F'], current_node['h'], current_node['g'])
            if new_child_nodes is None:
                continue
            
            print("OSF returned:", new_child_nodes, next_big_F)
            #new_child_nodes = [list(t) for t in new_child_nodes]
            #print(new_child_nodes)
            #new_child_nodes = [tuple(l) for l in new_child_nodes]
            #print(new_child_nodes)

            #for child in new_child_nodes:
            #    child = list(child)
            #    print(child)

            #new_child_nodes = list(new_child_nodes[0])
            
            for child in new_child_nodes:
                if child in visited:
                    continue
                #print(child)
                h = osf.list_of_locations_to_heuristic(child)
                g = current_node['g'] + num_agents
                small_f = g + h
                big_F = small_f
                new_node = {'agent_locs': child, 'g': g, 'h': h, 'small_f': small_f, 'big_F': big_F, 'parent': current_node}
                heappush(open_list, (new_node['big_F'], mycounter, new_node))
                mycounter+=1            
            if math.isinf(next_big_F):
                visited.add(current_node['agent_locs'])
            else:
                current_node['big_F'] = next_big_F
                heappush(open_list, (current_node['big_F'], mycounter, current_node))
                mycounter+=1
        return []
        
    def find_paths(self, node):
        path = []
        while (node['parent']):
            path.insert(0, node['parent']['agent_locs'])
            node = node['parent']
        path = [list(t) for t in path]
        path = list(list(i) for i in zip(*path))
        return path



