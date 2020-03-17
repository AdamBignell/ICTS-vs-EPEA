# Multi-value Design Diagram Class
# Used in ICTS
from collections import deque
from collections import defaultdict
import itertools

class MDD:
    def __init__(self, my_map, agent, start, goal, depth, generate = True):
        """ Note that in order to save memory, we do not store the map on each
        MDD, but instead pass the map as an argument to the generation function"""
        self.agent = agent
        self.start = start
        self.goal = goal
        self.depth = depth
        self.mdd = None
        self.level = defaultdict(list)
        if generate:
            self.generate_mdd(my_map)

    def generate_mdd(self, my_map):
        bfs_tree = self.get_depth_d_bfs_tree(my_map, self.start, self.goal, self.depth)
        mdd = self.bfs_to_mdd(bfs_tree, self.start, self.goal, self.depth)
        self.mdd = mdd
        if mdd:
            self.populate_levels(self.mdd)

    def populate_levels(self, mdd):
        self.level[0] = [self.start]
        for adjacent in mdd.values():
            for node in adjacent:
                self.level[node[1]].append(node[0])

    def get_level(self, i):
        if i > self.depth:
            return self.level[self.depth]
        return self.level[i]

    def get_depth_d_bfs_tree(self, my_map, start, goal, depth):
        # Run BFS to depth 'depth' to find the solutions for this agent
        fringe = deque()
        fringe.append((start, 0))
        prev_dict = defaultdict(list)
        visited = set()
        while fringe:
            curr = fringe.popleft()
            loc, d = curr
            if curr in visited:
                continue
            children = self.get_valid_children(my_map, loc, d)
            for c in children:
                if c[1] <= depth:
                    if curr not in prev_dict[c]:
                        prev_dict[c].append(curr)
                    fringe.append(c)
        return prev_dict

    def bfs_to_mdd(self, bfs_tree, start, goal, depth):
        # Convert a complete bfs tree to an mdd
        goal_time = (goal, depth)
        if not bfs_tree[goal_time]:
            return None
        mdd = defaultdict(list)
        trace_list = deque()
        for parent in bfs_tree[goal_time]:
            trace_list.append((parent, goal_time))
        while trace_list:
            curr, child = trace_list.popleft()
            if child not in mdd[curr]:
                mdd[curr].append(child)
            for p in bfs_tree[curr]:
                trace_list.append((p, curr))
        return mdd

    def get_valid_children(self, my_map, loc, d):
        # Get all children that are on the map
        x, y = loc[0], loc[1]
        all_children = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        good_children = []
        for c in all_children:
            if not my_map[c[0]][c[1]]:
                good_children.append((c, d+1))
        return good_children

# ========== Non-Class Functions Below ========== 

def is_solution_in_joint_mdd(mdds_list, return_solution = False):
    for mdd in mdds_list:
        if not mdd.mdd:
            return False
    roots = []
    depths = []
    for mdd in mdds_list:
        root = mdd.start
        roots.append(root)
        depths.append(mdd.depth)
    visited = set()
    roots_key = tuple(roots)
    if not return_solution:
        found_path, visited = joint_mdd_dfs(mdds_list, (roots_key, 0), max(depths), visited)
        return found_path
    # else == return_solution
    solution, visited = joint_mdd_dfs_return_solution(mdds_list, (roots_key, 0), max(depths), visited)
    return solution

def find_solution_in_joint_mdd(mdds_list):
    solution = is_solution_in_joint_mdd(mdds_list, True)
    return joint_mdd_nodes_to_list_of_paths(solution)

def joint_mdd_dfs(mdds_list, curr, max_depth, visited):
    curr_nodes = curr[0]
    curr_depth = curr[1]
    if curr in visited or curr_depth > max_depth:
        return False, visited

    visited.add(curr)
    if is_goal_state(mdds_list, curr_nodes, curr_depth):
        return True, visited
    
    valid_children = get_valid_children(mdds_list, curr_nodes, curr_depth)

    # DFS below
    for node in valid_children:
        child = (node, curr_depth+1)
        # Checking if a solution exists
        found_path, visited = joint_mdd_dfs(mdds_list, child, max_depth, visited)
        if found_path:
            return found_path, visited
    return False, visited

def joint_mdd_dfs_return_solution(mdds_list, curr, max_depth, visited):
    curr_nodes = curr[0]
    curr_depth = curr[1]
    if curr in visited or curr_depth > max_depth:
        return [], visited

    visited.add(curr)
    if is_goal_state(mdds_list, curr_nodes, curr_depth):
        return [curr], visited
    
    valid_children = get_valid_children(mdds_list, curr_nodes, curr_depth)

    # DFS below
    partial_solution = [curr]
    for node in valid_children:
        child = (node, curr_depth+1)
        # Finding a solution
        solution, visited = joint_mdd_dfs_return_solution(mdds_list, child, max_depth, visited)
        if solution != []:
            partial_solution.extend(solution)
            return partial_solution, visited
    return [], visited
    
def is_goal_state(mdds_list, curr_nodes, curr_depth):
    for i, node in enumerate(curr_nodes):
        this_mdd = mdds_list[i]
        if curr_depth < this_mdd.depth or this_mdd.goal != node:
            return False
    return True

def get_valid_children(mdds_list, curr_nodes, curr_depth):
    all_indiv_children = get_children_for_cross_prod(mdds_list, curr_nodes, curr_depth)
    all_joint_child_nodes = list(itertools.product(*all_indiv_children))
    pruned_joint_child_nodes = prune_joint_children(all_joint_child_nodes, curr_nodes)
    return pruned_joint_child_nodes

def get_children_for_cross_prod(mdds_list, curr_nodes, curr_depth):
    all_indiv_children = []
    for i, node in enumerate(curr_nodes):
        this_mdd = mdds_list[i]
        if this_mdd.goal == node and curr_depth == this_mdd.depth:
            all_indiv_children.append([this_mdd.goal])
            continue
        i_children = this_mdd.mdd[(node, curr_depth)]
        i_children_locs = [i_child[0] for i_child in i_children]
        all_indiv_children.append(i_children_locs)
    return all_indiv_children
    
def prune_joint_children(all_joint_nodes, curr_nodes):

    # print("All Joint Child Nodes = ", all_joint_nodes)
    all_joint_child_nodes = []
    for node in all_joint_nodes:
        if len(set(node)) == len(node) and not has_edge_collisions(curr_nodes, node):
            all_joint_child_nodes.append(node)
    return all_joint_child_nodes

def has_edge_collisions(curr_nodes, next_nodes):
    forward = [pair for pair in zip(curr_nodes, next_nodes) if pair[0] != pair[1]]
    backward = [pair for pair in zip(next_nodes, curr_nodes) if pair[0] != pair[1]]
    edge_collisions = set(forward).intersection(set(backward))
    return len(edge_collisions) > 0

def joint_mdd_nodes_to_list_of_paths(mdd_nodes):
    if not mdd_nodes or not mdd_nodes[0]:
        return None
    num_agents = len(mdd_nodes[0][0])
    paths = [[] for i in range(num_agents)]
    for node in mdd_nodes:
        for i, loc in enumerate(node[0]):
            paths[i].append(loc)
    return paths