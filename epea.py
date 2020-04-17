import time as timer
from heapq import heappush
from heapq import heappop
import random
from osf import OSF
from map_utils import MapDetails
from performance_tracker import PerformanceTracker
import math

class EPEASolver(object):
    """A high-level EPEA* search."""

    def __init__(self, map_details):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """
        self.my_map = map_details.map_instance
        self.starts = map_details.starting_loc
        self.goals = map_details.goal_loc
        self.num_of_agents = len(map_details.goal_loc)

        self.num_of_agents = len(self.goals)

        self.open_list = []
        self.visited = set()
        self.visited_loc_Big_f = set()

        self.osf = OSF(self.my_map, self.goals)

        self.stat_tracker = PerformanceTracker()
        self.stat_tracker.set_map_name(map_details.name)
        self.stat_tracker.set_results_file_name(map_details.result_file_name)

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations
        """
        print("\nFinding EPEA* Solution...")
        result = self.stat_tracker.time("time", lambda: self.epea_star())
        self.stat_tracker.write_stats_to_file(self.stat_tracker.get_results_file_name())
        return result
    
    def epea_star(self):
        osf = self.osf
        open_list = self.open_list
        start_locs = tuple(self.starts)
        goals = self.goals
        visited_locs = self.visited
        visited_loc_Big_f = self.visited_loc_Big_f
        num_agents = len(start_locs)
        mycounter = 0       # counter used to break ties in the priority queue
        g = 0
        h = osf.list_of_locations_to_heuristic(start_locs)

        start_node = {'agent_locs': start_locs, 'g': 0, 'h': h, 'small_f': g + h, 'big_F': g + h, 'parent': False}
        priority_tuple = (g + h, h, -g, mycounter)
        heappush(open_list, (priority_tuple, start_node))
        mycounter+=1
        while(len(open_list) != 0):
            priority_tuple, current_node = heappop(open_list)
            if current_node['agent_locs'] in visited_loc_Big_f:
                continue
            if list(current_node['agent_locs']) == goals:
                return self.find_paths(current_node, goals)
            #print(current_node['agent_locs'], priority_tuple)
            new_child_nodes, next_big_F = osf.get_children_and_next_F(current_node)
            for child in new_child_nodes:
                if child in visited_locs:
                    continue
                h = osf.list_of_locations_to_heuristic(child)
                g = current_node['g'] + num_agents
                small_f = g + h
                big_F = small_f
                new_node = {'agent_locs': child, 'g': g, 'h': h, 'small_f': small_f, 'big_F': big_F, 'parent': current_node}
                visited_locs.add(child)
                visited_loc_Big_f.add((child, big_F))
                priority_tuple = (big_F, h, -g, mycounter)
                heappush(open_list, (priority_tuple, new_node))
                mycounter+=1            
            if math.isinf(next_big_F):
                visited_locs.add(current_node['agent_locs'])
            else:
                current_node['big_F'] = next_big_F
                priority_tuple = (current_node['big_F'], current_node['h'], -current_node['g'], mycounter)
                heappush(open_list, (priority_tuple, current_node))
                visited_loc_Big_f.add((current_node['agent_locs'], next_big_F))
                mycounter+=1
        return []
        
    def find_paths(self, node, goals):
        path = [goals]
        while (node['parent']):
            path.append(node['parent']['agent_locs'])
            node = node['parent']
        path.reverse()
        path = [list(t) for t in path]
        path = list(list(i) for i in zip(*path))
        return path



