# Multi-value Design Diagram Class
# Used in ICTS
from collections import deque
from collections import defaultdict

class MDD:
    def __init__(self, my_map, agent, start, goal, depth, generate = True):
        """ Note that in order to save memory, we do not store the map on each
        MDD, but instead pass the map as an argument to the generation function"""
        self.agent = agent
        self.start = start
        self.goal = goal
        self.depth = depth
        self.mdd = None
        if generate:
            self.generate_mdd(my_map, agent, start, goal, depth)

    def generate_mdd(self, my_map, agent, start, goal, depth):
        bfs_tree = self.get_depth_d_bfs_tree(my_map, agent, start, goal, depth)
        mdd = self.bfs_to_mdd(bfs_tree, start, goal, depth)
        self.mdd = mdd

    def get_depth_d_bfs_tree(self, my_map, agent, start, goal, depth):
        # Run BFS to find the solutions for this agent
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
        goal_time = (goal, depth)
        if not bfs_tree[goal_time]:
            return None
        mdd = defaultdict(list)
        trace_list = deque()
        for parent in bfs_tree[goal_time]:
            trace_list.append((parent, goal_time))
        print(trace_list)
        while trace_list:
            curr, child = trace_list.popleft()
            if child not in mdd[curr]:
                mdd[curr].append(child)
            for p in bfs_tree[curr]:
                trace_list.append((p, curr))
        return mdd

    def get_valid_children(self, my_map, loc, d):
        x, y = loc[0], loc[1]
        all_children = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        good_children = []
        for c in all_children:
            if not my_map[c[0]][c[1]]:
                good_children.append((c, d+1))
        return good_children

