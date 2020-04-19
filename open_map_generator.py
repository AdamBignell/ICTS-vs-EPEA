import argparse
import copy
from random import random, randrange, seed
from datetime import datetime as dt

OPEN_SPACE = 0
OBSTACLE = 1
START_OR_GOAL = 2

RIGHTMOST_BORDER_FORMAT = '@\n'
OPEN_SPACE_FORMAT = '. '
OBSTACLE_SPACE_FORMAT = '@ '

PROBABILITY_OF_BECOMING_OBSTACLE = 0.1

def create_initial_map(rows, cols):
    new_map = [[OPEN_SPACE] * cols for x in range(rows)]
    new_map = create_border_for_map(new_map)
    return new_map

def create_border_for_map(map):
    bordered_map = map
    num_rows = len(map)
    num_cols = len(map[0])

    max_row = num_rows - 1
    max_col = num_cols - 1

    for row in range(num_rows):
        for col in range(num_cols):
            if position_is_on_border(row, col, max_row, max_col):
                bordered_map[row][col] = OBSTACLE

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
        random_location = (randrange(min_row, max_row + 1), randrange(min_col, max_col + 1))

        if not random_location in existing_locations:
            finding_new_location = False

    return random_location

def mark_start_and_goal_locations(locations, map):
    locations = locations['start_loc'] + locations['goal_loc']

    for location in locations:
        map[location[0]][location[1]] = START_OR_GOAL

    return map

def format_start_and_goal_to_string(start, goal):
    return '{0} {1} {2} {3}\n'.format(start[0], start[1], goal[0], goal[1])

def format_all_start_and_goal_locations(locations):
    start_loc = locations['start_loc']
    goal_loc = locations['goal_loc']
    formatted_start_and_goals = ''

    for i in range(len(start_loc)):
        formatted_start_and_goals = formatted_start_and_goals + format_start_and_goal_to_string(start_loc[i], goal_loc[i])

    return formatted_start_and_goals

def convert_logical_map_to_string(logical_map):
    string_map = ''

    num_rows = len(logical_map)
    num_cols = len(logical_map[0])
    max_row = num_rows - 1

    for row in range(num_rows):
        for col in range(num_cols):
            current_value = logical_map[row][col]
            equivalent_string_format = convert_single_logical_value_to_single_string_format(current_value, col, max_row)
            string_map = string_map + equivalent_string_format

    return string_map

def convert_single_logical_value_to_single_string_format(logical_value, column, max_row):
    equivalent_string_format = ''

    if column == max_row:
        equivalent_string_format = RIGHTMOST_BORDER_FORMAT
    elif logical_value == OBSTACLE:
        equivalent_string_format = OBSTACLE_SPACE_FORMAT
    else:
        equivalent_string_format = OPEN_SPACE_FORMAT

    return equivalent_string_format

def generate_random_obstacles(logical_map, probability_of_switching_to_obstacle):
    num_rows = len(logical_map)
    num_cols = len(logical_map[0])

    for row in range(1, num_rows):
        for col in range(1, num_cols):
            if random() < probability_of_switching_to_obstacle:
                logical_map[row][col] = OBSTACLE

    return logical_map

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a randomly generated open map')
    parser.add_argument('--output', type=str, default=None,
                        help='The name of the output file')
    parser.add_argument('--dim', type=int, nargs='+',
                        help="The dimension of the map")
    parser.add_argument('--agents', type=int,
                        help="The number of agents")

    args = parser.parse_args()
    seed(dt.now())

    rows = args.dim[0]
    cols = args.dim[1]
    random_open_map = create_initial_map(rows, cols)
    map_without_border = [[0] * (cols - 2) for x in range(rows - 2)]

    start_and_goal_loc = generate_starting_and_goal_locations(map_without_border, 3)
    random_open_map = mark_start_and_goal_locations(start_and_goal_loc, random_open_map)
    random_open_map = generate_random_obstacles(random_open_map, PROBABILITY_OF_BECOMING_OBSTACLE)

    map_number = 1
    file_name = 'open_maps/open{0}x{1}_{2}_{3}.txt'.format(args.dim[0], args.dim[1], args.agents, map_number)
    f = open(file_name, 'w')
    string_to_write_to_file = '{0} {1}\n'.format(args.dim[0], args.dim[1])
    string_to_write_to_file = string_to_write_to_file + convert_logical_map_to_string(random_open_map)
    string_to_write_to_file = string_to_write_to_file + '{0}\n'.format(args.agents)
    string_to_write_to_file = string_to_write_to_file + format_all_start_and_goal_locations(start_and_goal_loc)
    f.write(string_to_write_to_file)
    f.close()
