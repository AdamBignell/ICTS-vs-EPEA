from single_agent_planner import compute_heuristics, a_star
from ict import IncreasingCostTree
from mdd import MDD, find_solution_in_joint_mdd
from map_utils import find_number_of_open_spaces
from performance_tracker import PerformanceTracker
import collections
import time as timer

class ICTSSolver(object):
    """A high-level ICTS search."""

    def __init__(self, map_details):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = map_details.map_instance
        self.starts = map_details.starting_loc
        self.goals = map_details.goal_loc
        self.num_of_agents = len(map_details.goal_loc)

        self.stat_tracker = PerformanceTracker("ICTS")
        self.stat_tracker.set_map_name(map_details.name)
        self.stat_tracker.set_results_file_name(map_details.result_file_name)

        self.open_list = []

        # compute heuristics for the low-level search
        self.heuristics = []
        self.stat_tracker.time("heuristic_time", lambda: self.calculate_heuristics())

        self.ict = self.stat_tracker.time("time", lambda: self.create_ict())
        self.upper_bound = self.calculate_upper_bound_cost()

    def calculate_heuristics(self):
        for goal in self.goals:
            self.heuristics.append(self.true_distance_bfs(self.my_map, goal))

    def true_distance_bfs(self, my_map, goal):
        h = dict()
        q = collections.deque()
        indiv_ops = [(1, 0), (-1, 0), (0, 1), (0, -1), (0, 0)]
        q.append((goal, 0))
        visited = set()
        visited.add(goal)
        while q:
            (x,y), this_h = q.popleft()
            h[(x,y)] = this_h
            children = []
            for op in indiv_ops:
                new_child = (x+op[0], y+op[1])
                if not my_map[new_child[0]][new_child[1]] and new_child not in visited:
                    visited.add(new_child)
                    children.append((new_child, this_h+1))
            if children:
                q.extend(children)
        return h

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations
        """
        print("\nFinding ICTS Solution...")
        ######### Fill in the ICTS Algorithm here #########
        result = self.stat_tracker.time("time", lambda: self.bfs())
        if result == -1:
            self.stat_tracker.stats['time'] = -1
            return []
        self.stat_tracker.write_stats_to_file(self.stat_tracker.get_results_file_name())
        return result
        ###################################################

    def calculate_upper_bound_cost(self):
        number_of_open_spaces = find_number_of_open_spaces(self.my_map)
        upper_bound = (self.num_of_agents ** 2) * number_of_open_spaces
        return upper_bound

    def bfs (self):
        ict = self.ict
        open_list = ict.get_open_list()
        mdd_cache = {}
        start_time = timer.time()
        nodes_expanded = 0
        while(len(open_list) != 0):
            current_node = ict.get_next_node_to_expand()
            node_cost = current_node.get_cost()
            if timer.time() - start_time > 300:
                return -1
            self.print_sanity_track(start_time, nodes_expanded)
            if not self.node_has_exceeded_upper_bound(current_node, self.upper_bound):
                solution_paths = self.find_paths_for_agents_for_given_cost(node_cost, mdd_cache)
                if(self.solution_exists(solution_paths)):
                    return solution_paths
                else:
                    self.stat_tracker.count('expanded nodes', lambda: ict.expand_next_node())
                    nodes_expanded += 1
            ict.pop_next_node_to_expand()
        return []

    def node_has_exceeded_upper_bound(self, node, upper_bound):
        agent_costs = node.get_cost()
        summed_agent_costs = sum(agent_costs)

        return summed_agent_costs > upper_bound

    def solution_exists(self, paths):
        return paths != None

    def find_paths_for_agents_for_given_cost(self, agent_path_costs, mdd_cache):
        mdds = []
        for i in range(len(agent_path_costs)):
            agent_depth_key = (i, agent_path_costs[i])
            if agent_depth_key not in mdd_cache:
                agent_prev_depth_key = (i, agent_path_costs[i]-1)
                t1 = timer.time()
                if agent_prev_depth_key in mdd_cache:
                    new_mdd = MDD(self.my_map, i, self.starts[i], self.goals[i], agent_path_costs[i], last_mdd = mdd_cache[agent_prev_depth_key])
                else:
                    new_mdd = MDD(self.my_map, i, self.starts[i], self.goals[i], agent_path_costs[i])
                t2 = timer.time()
                mdd_cache[agent_depth_key] = new_mdd
            else: # Already cached
                new_mdd = mdd_cache[agent_depth_key]
            mdds.append(new_mdd)
        t1 = timer.time()
        solution_path = find_solution_in_joint_mdd(mdds)
        t2 = timer.time()
        return solution_path 

    def create_ict(self):
        initial_estimate = self.find_cost_of_initial_estimate_for_root()
        if not initial_estimate:
            return None
        ict = IncreasingCostTree(self.my_map, self.starts, self.goals, initial_estimate)

        return ict

    def find_cost_of_initial_estimate_for_root(self):
        optimal_paths = self.find_most_optimal_paths()
        optimal_costs = []

        for i in range(len(optimal_paths)):
            if not optimal_paths[i]:
                return []
            optimal_costs.append(max(len(optimal_paths[i]) - 1, 0))

        return optimal_costs

    def find_most_optimal_paths(self):
        optimal_paths = []
        for agent in range(self.num_of_agents):
            optimal_paths.append(a_star(self.my_map, self.starts[agent], self.goals[agent], self.heuristics[agent], agent, []))
        return optimal_paths

    def print_sanity_track(self, start_time, num_expanded):
        elapsed = "{:.5f}".format(round(timer.time()-start_time, 5))
        print("\r[ Time elapsed: " + elapsed + "s | Nodes expanded: " + str(num_expanded), end=" ]", flush=True)
