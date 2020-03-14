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
        self.open_list = [self.root]

    def get_open_list(self):
        return self.open_list

    def get_next_node_to_expand(self):
        return self.open_list.pop(0)


class TreeNode:
    def __init__(self, agent_path_costs):
        self.agent_path_costs = agent_path_costs
        self.child_nodes = []

    def get_cost(self):
        return self.agent_path_costs

    def get_ith_child(self, i):
        return self.child_nodes[i]

    def get_all_children(self):
        return self.child_nodes

    def add_child(self, new_agent_path_costs):
        new_child = TreeNode(new_agent_path_costs)
        self.child_nodes.append(new_child)

    def expand_node(self):
        for i in range(len(self.agent_path_costs)):
            new_costs = copy.deepcopy(self.agent_path_costs)
            new_costs[i] = new_costs[i] + 1
            new_child = TreeNode(new_costs)
            self.child_nodes.append(new_child)