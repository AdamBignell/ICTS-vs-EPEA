import time as timer
from heapq import heappush
from heapq import heappop
import random
from osf import OSF
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

        # compute heuristics for the low-level search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

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
        num_agents = len(start_locs)

        g = 0
        h = osf.list_of_locations_to_heuristic(start_locs)

        #for agent, loc in enumerate(starts):
        #    h += osf.h[agent][starts[agent][0]][starts[agent][1]]

        start_node = {'agent_locs': start_locs, 'g': 0, 'h': h, 'small_f': g + h, 'big_F': g + h}
        heappush(open_list, start_node)
        while(len(open_list) != 0):
            current_node = heappop(open_list)
            if current_node['agent_locs'] == goals:
                return "success"        # to be implemented: returning path etc.
            
            #set something to value of OSF? not sure what goes here -> OSF returns list of all children locations, and the "next cost", F_Next
            new_child_nodes, next_big_F = osf.get_children_and_next_F(current_node['agent_locs'], current_node['big_F'], current_node['h'], current_node['g'])

            for child in new_child_nodes:
                h = osf.list_of_locations_to_heuristic(child)
                g = current_node['g'] + num_agents
                small_f = 

                compute_heuristics(child)
                compute_cost(child)
                #not sure what the next few lines mean (for PEA*, disregard)
                #if f(n_c) != F(n):
                    #if f(n_c) > F(n):
                        #F_next(n) = min(F_next(n), f(n_c))
                        #discard n_c
                        #continue
                #check for duplicates
            
            #if F_next(n) = inf:
                #put n into closed
            #else:
                #F(n) = F_next(n)
                self.open_list.append(curr)

            return None
        ###################################################
    
    def collapse(self, node):
        pass

    def get_lowest_stored_cost(self, open_list):
        pass
    
    def generate_children(self, node):
        pass
    
    def compute_cost(self, node):
        pass

