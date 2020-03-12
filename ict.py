import copy

class IncreasingCostTree:
    def __init__(self, my_map, starts, goals, initial_cost):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.initial_cost = initial_cost
        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)
        self.root = TreeNode(self.initial_cost)
        self.open_list = []

class TreeNode:
    def __init__(self, agent_path_costs):
        self.agent_path_costs = agent_path_costs
        self.child_nodes = []

    def get_ith_child(self, i):
        return self.childNodes[i]

    def get_all_children(self):
        return self.child_nodes

    def add_child(self, new_agent_path_costs):
        new_child = TreeNode(new_agent_path_costs)
        self.child_nodes.append(new_child)

    def expand_node(self, number_of_children_to_create):
        for i in range(number_of_children_to_create):
            new_costs = copy.deepcopy(self.initial_cost)
            new_costs[i] = new_costs[i] + 1
            new_child = TreeNode(new_costs)
            self.children.append(new_child)