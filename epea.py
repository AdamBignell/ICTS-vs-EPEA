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

        self.stat_tracker = PerformanceTracker("EPEA")
        self.stat_tracker.set_map_name(map_details.name)
        self.stat_tracker.set_results_file_name(map_details.result_file_name)

        self.osf = self.stat_tracker.time("osf time", lambda: OSF(self.my_map, self.goals))

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
        goals = tuple(self.goals)
        visited_locs = self.visited
        num_agents = len(start_locs)
        mycounter = 0 # counter used to break ties in the priority queue
        g = 0
        h = osf.list_of_locations_to_heuristic(start_locs)

        start_node = {'agent_locs': start_locs, 'g': 0, 'h': h, 'small_f': g + h, 'big_F': g + h, 'parent': False}
        priority_tuple = (g + h, -g, h, mycounter)
        heappush(open_list, (priority_tuple, start_node))
        mycounter+=1
        start_time = timer.time()
        nodes_expanded = 0
        while(len(open_list) != 0):
            self.print_sanity_track(start_time, nodes_expanded)
            priority_tuple, current_node = heappop(open_list)
            if current_node['agent_locs'] == goals:
                return self.find_paths(current_node, goals)
            new_child_nodes, next_big_F = self.stat_tracker.count("expanded nodes", lambda: osf.get_children_and_next_F(current_node))
            for child in new_child_nodes:
                child_node = self.get_child_node(child, current_node, osf)
                if child not in visited_locs:
                    visited_locs.add(child)
                    priority_tuple = (child_node['big_F'], child_node['h'], -child_node['g'], mycounter)
                    heappush(open_list, (priority_tuple, child_node))
                    self.stat_tracker.record_max('max_open_list_length', len(open_list))
                    mycounter+=1
            if math.isinf(next_big_F):
                visited_locs.add(current_node['agent_locs'])
            else:
                current_node['big_F'] = next_big_F
                priority_tuple = (current_node['big_F'], current_node['h'], -current_node['g'], mycounter)
                heappush(open_list, (priority_tuple, current_node))
                self.stat_tracker.record_max('max_open_list_length', len(open_list))
                mycounter +=1
            nodes_expanded += 1
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

    def print_sanity_track(self, start_time, num_expanded):
        elapsed = "{:.5f}".format(round(timer.time()-start_time, 5))
        print("\r[ Time elapsed: " + elapsed + "s | Nodes expanded: " + str(num_expanded), end=" ]", flush=True)

    def get_child_node(self, child, parent, osf):
        h = osf.list_of_locations_to_heuristic(child)
        num_agents_not_at_goal = 0
        for i, loc in enumerate(child):
            if self.goals[i] != loc:
                num_agents_not_at_goal += 1
        g = parent['g'] + num_agents_not_at_goal
        small_f = g + h
        big_F = small_f
        new_node = {'agent_locs': child, 'g': g, 'h': h, 'small_f': small_f, 'big_F': big_F, 'parent': parent}
        return new_node