from single_agent_planner import compute_heuristics, a_star
from ict import IncreasingCostTree
from mdd import MDD, find_solution_in_joint_mdd
from map_utils import find_number_of_open_spaces

class ICTSSolver(object):
    """A high-level ICTS search."""

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

        self.ict = self.create_ict()
        self.upper_bound = self.calculate_upper_bound_cost()

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations
        """
        print("\nFinding ICTS Solution...")
        ######### Fill in the ICTS Algorithm here #########
        return self.bfs()
        ###################################################

    def calculate_upper_bound_cost(self):
        number_of_open_spaces = find_number_of_open_spaces(self.my_map)
        upper_bound = 0

        for i in range(self.num_of_agents):
            upper_bound = upper_bound + ((i + 1) * (number_of_open_spaces))

        return upper_bound

    def bfs (self):
        ict = self.ict
        open_list = ict.get_open_list()

        while(len(open_list) != 0):
            current_node = ict.get_next_node_to_expand()
            node_cost = current_node.get_cost()
            solution_paths = self.find_paths_for_agents_for_given_cost(node_cost)

            if(self.solution_exists(solution_paths)):
                return solution_paths
            elif not self.node_has_exceeded_upper_bound(current_node, self.upper_bound):
                ict.expand_next_node()

            ict.pop_next_node_to_expand()

        print("Could not find solution")
        return []

    def node_has_exceeded_upper_bound(self, node, upper_bound):
        agent_costs = node.get_cost()
        summed_agent_costs = sum(agent_costs)

        return summed_agent_costs > upper_bound

    def solution_exists(self, paths):
        return paths != None

    def find_paths_for_agents_for_given_cost(self, agent_path_costs):
        mdds = []

        for i in range(len(agent_path_costs)):
            new_mdd = MDD(self.my_map, i, self.starts[i], self.goals[i], agent_path_costs[i])
            mdds.append(new_mdd)

        solution_path = find_solution_in_joint_mdd(mdds)
        return solution_path

    def create_ict(self):
        initial_estimate = self.find_cost_of_initial_estimate_for_root()
        ict = IncreasingCostTree(self.my_map, self.starts, self.goals, initial_estimate)

        return ict

    def find_cost_of_initial_estimate_for_root(self):
        optimal_paths = self.find_most_optimal_paths()
        optimal_costs = []

        for i in range(len(optimal_paths)):
            optimal_costs.append(max(len(optimal_paths[i]) - 1, 0))

        return optimal_costs

    def find_most_optimal_paths(self):
        optimal_paths = []

        for agent in range(self.num_of_agents):
            optimal_paths.append(a_star(self.my_map, self.starts[agent], self.goals[agent], self.heuristics[agent], agent, []))

        return optimal_paths
