import time as timer
import heapq
import random
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

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations
        """
        print("\nFinding EPEA* Solution...")
        ######## Fill in the EPEA* Algorithm here #########

        start_node = starts
        compute_heuristics(start_node)
        self.open_list.append(start_node)
        while(len(self.open_list) != 0):
            current_node = get_lowest_stored_cost(open_list)
            if current_node == goal_state:
                return "success"
            #set something to value of OSF? not sure what goes here
            #(N, F_next(n)) = OSF(n)
            for child in generate_children(current_node):
                compute_heuristics(child)
                compute_cost(child)
                #not sure what the next few lines mean
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

