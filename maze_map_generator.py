import random
import collections
import argparse
import os
from datetime import datetime as dt
import os

kGrowRate = 0.75
kBridgeRate = 0
random.seed(dt.now())
kFilledRate = 0.25
kMazeDirectory = "mazes/"

def generate_maze_to_file(x, y, num_agents, file_name):
    maze, open_cells = get_maze(x, y, num_agents, kFilledRate)
    agent_locs = get_agent_starts_and_goals(open_cells, num_agents)
    write_to_file(x, y, maze, agent_locs, file_name)

def get_maze(x, y, num_agents, filled_rate):
    open_cells = []
    while len(open_cells) < filled_rate * x * y:
        maze = [['@' for i in range(y)] for j in range(x)]
        open_cells = set()
        maze, seeds = seed_maze_root(maze)
        maze = grow_maze(maze, seeds, kGrowRate)
        #maze = bridge_maze(maze, kBridgeRate)
        open_cells = get_open(maze)
    return maze, open_cells
        
def get_agent_starts_and_goals(open_cells, num_agents):
    random.shuffle(open_cells)
    agent_start_goal = []
    for i in range(num_agents):
        agent_start = open_cells.pop()
        start_string = str(agent_start[0]) + " " + str(agent_start[1]) + " "
        agent_goal = open_cells.pop()
        goal_string = str(agent_goal[0]) + " " + str(agent_goal[1])
        agent_start_goal.append(start_string + goal_string)
    return agent_start_goal

def seed_maze_multiple(maze, seed_rate):
    x = len(maze)
    y = len(maze[0])
    num_to_seed = int(round(len(maze)*len(maze[0])*seed_rate))
    i = 0
    seeds = []
    while i < num_to_seed:
        rand_x = random.randint(1, x-2)
        rand_y = random.randint(1, y-2)
        if maze[rand_x][rand_y] == '.':
            continue
        else:
            maze[rand_x][rand_y] = '.'
            i += 1
            seeds.append((rand_x,rand_y))
    return maze, seeds

def seed_maze_root(maze):
    x = len(maze)
    y = len(maze[0])
    rand_x = random.randint(1, x-2)
    rand_y = random.randint(1, y-2)
    maze[rand_x][rand_y] = '.'
    return maze, [(rand_x, rand_y)]

def get_children(max_x, max_y, x, y, diag=False):
    children = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    if diag:
        children.extend([(x-1, y-1), (x+1, y+1), (x-1, y+1), (x+1, y-1)])
    good_children = []
    for child in children:
        c_x, c_y = child
        if c_x >= max_x-1 or c_x <= 0 or c_y >= max_y-1 or c_y <= 0:
            continue
        good_children.append(child)
    return good_children
            

def grow_maze(maze, seeds, growRate):
    open = collections.deque()
    open.extend(seeds)
    visited = set()
    while open:
        (x,y) = open.popleft()
        visited.add((x,y))
        if count_open_neighbours(maze, x, y) < 2:
            maze[x][y] = "."
        else:
            continue
        children = get_children(len(maze), len(maze[0]), x, y)
        for child in children:
            (c_x, c_y) = child
            flip = random.uniform(0, 1)
            if (c_x, c_y) not in visited and flip <= growRate:
                open.append(child)
    return maze

def bridge_maze(maze, bridge_rate):
    num_open = 0
    for x, row in enumerate(maze[:-1]):
        if x == 0:
            continue
        for y, cell in enumerate(row[:-1]):
            if y == 0:
                continue
            flip = random.uniform(0,1)
            if cell == '@' and flip < bridge_rate and count_open_neighbours(maze, x, y) <= 3 and count_open_neighbours(maze, x, y) > 1:
                maze[x][y] = '.'
    return maze
    
def count_open_neighbours(maze, x, y, diag=False):
    neighbours = get_children(len(maze), len(maze[0]), x, y, diag)
    num_open = 0
    for (n_x, n_y) in neighbours:
        if maze[n_x][n_y] == '.':
            num_open += 1
    return num_open

def get_open(maze):
    num_open = []
    for x, row in enumerate(maze):
        for y, cell in enumerate(row):
            if cell == '.':
                num_open.append((x,y))
    return num_open

def write_to_file(x, y, maze, agent_locs, file_name):
    my_dir = os.getcwd()
    full_file = my_dir + "/" + kMazeDirectory + file_name
    with open(full_file, mode='w') as file:
        file.write(str(x) + " " + str(y) + '\n')
        print_maze(maze, file)
        file.write('\n' + str(len(agent_locs)) + '\n')
        for line in agent_locs:
            file.write(line + '\n')

def print_maze(maze, file):
    for x, row in enumerate(maze):
        for y, cell in enumerate(row):
            file.write(cell + ' ')
        if x != len(maze)-1:
            file.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a randomly generated open map')
    parser.add_argument('--dim', type=int, nargs='+',
                        help="The dimension of the map")
    parser.add_argument('--agents', type=int,
                        help="The number of agents")
    parser.add_argument('--startnum', type=int,
                        help="The starting number for the naming convention")
    parser.add_argument('--nummaps', type=int,
                        help="The number of maps to generate")
    parser.add_argument('--probability', type=float,
                        help="The probability a direction will be opened")
    parser.add_argument('--bridgeprobability', type=float,
                        help="The probability two unconnected corridors will be bridged together")

    args = parser.parse_args()

    kGrowRate = args.probability
    kBridgeRate = args.bridgeprobability
    
    for i in range(args.startnum, args.startnum + args.nummaps):
        name_string = "maze" + str(args.dim[0]) + "x" + str(args.dim[1]) + "_" + str(args.agents) + "_" + str(i) + ".txt"
        generate_maze_to_file(args.dim[0], args.dim[1], args.agents, name_string)
    
