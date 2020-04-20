import copy
import collections

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

        self.open_list = collections.deque() 
        self.open_list.append(self.root)
        self.closed_list = set(initial_cost)

    def get_open_list(self):
        return self.open_list

    def get_next_node_to_expand(self):
        return self.open_list[0]

    def pop_next_node_to_expand(self):
        return self.open_list.popleft()

    def add_node_to_open_list(self, node):
        self.open_list.append(node)

    def add_unexplored_node_to_open_list(self, node):
        node_cost = node.get_cost()
        node_has_been_visited = node_cost in self.closed_list

        if not node_has_been_visited:
            self.closed_list.add(node_cost)
            self.open_list.append(node)

    def expand_next_node(self):
        next_node = self.get_next_node_to_expand()
        next_node.expand_node()
        children = next_node.get_all_children()
        for child in children:
            self.add_unexplored_node_to_open_list(child)

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
            new_costs = list(copy.deepcopy(self.agent_path_costs))
            new_costs[i] = new_costs[i] + 1
            new_child = TreeNode(tuple(new_costs))
            self.child_nodes.append(new_child)