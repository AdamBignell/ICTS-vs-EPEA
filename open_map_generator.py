import argparse
import copy

from random import randrange

def create_initial_map(rows, cols):
    map = [[0] * cols for x in range(rows)]
    map = create_border_for_map(map)
    return map

def create_border_for_map(map):
    bordered_map = map
    num_rows = len(map)
    num_cols = len(map[0])

    max_row = num_rows - 1
    max_col = num_cols - 1

    for row in range(num_rows):
        for col in range(num_cols):
            if position_is_on_border(row, col, max_row, max_col):
                bordered_map[row][col] = 1

    return bordered_map

def position_is_on_border(row, col, max_row, max_col):
    return row == 0 or col == 0 or row == max_row or col == max_col

def generate_starting_and_goal_locations(map, num_of_agents):
    all_locations = set()
    starting_locations = list()
    goal_locations = list()
    num_of_starting_locations = copy.deepcopy(num_of_agents)
    num_of_goal_locations = copy.deepcopy(num_of_agents)

    for starts in range(num_of_starting_locations):
        random_location = generate_new_random_location(all_locations, map)
        all_locations.add(random_location)
        starting_locations.append(random_location)

    for goals in range(num_of_goal_locations):
        random_location = generate_new_random_location(all_locations, map)
        all_locations.add(random_location)
        goal_locations.append(random_location)

    important_locations = {'start_loc': starting_locations, 'goal_loc': goal_locations}
    return important_locations

def generate_new_random_location(existing_locations, map):
    finding_new_location = True
    min_row = 1
    min_col = 1
    max_row = len(map)
    max_col = len(map[0])
    random_location = (-1, -1)

    while finding_new_location:
        random_location = (randrange(min_row, max_row + 1), randrange(min_col, max_col + 1)) # problem with rand range?

        if not random_location in existing_locations:
            finding_new_location = False

    return random_location

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a randomly generated open map')
    parser.add_argument('--output', type=str, default=None,
                        help='The name of the output file')
    parser.add_argument('--dim', type=int, nargs='+',
                        help="The dimension of the map")
    parser.add_argument('--agents', type=int,
                        help="The number of agents")

    args = parser.parse_args()

    rows = args.dim[0]
    cols = args.dim[1]
    random_open_map = create_initial_map(rows, cols)
    map_without_border = [[0] * (cols - 2) for x in range(rows - 2)]

    start_and_goal_loc = generate_starting_and_goal_locations(map_without_border, 3)

    f = open(args.output, 'w')
    f.write('{0} {1}\n'.format(args.dim[0], args.dim[1]))
    f.close()

