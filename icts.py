from single_agent_planner import compute_heuristics, a_star
from ict import IncreasingCostTree

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

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations
        """
        print("\nFinding ICTS Solution...")
        ######### Fill in the ICTS Algorithm here #########
        return self.bfs()
        ###################################################

    def bfs (self):
        ict = self.ict
        open_list = ict.get_open_list()

        while(len(open_list) != 0):
            current_node = ict.get_next_node_to_expand()

            if(self.node_contains_solution(current_node)):
                return current_node
            else:
                ict.expand_next_node()

        return "Could not find solution"


    def node_contains_solution(self, node):
        return False

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
