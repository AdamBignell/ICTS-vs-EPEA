import argparse

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
    map_without_border = [[0] * (cols - 1) for x in range(rows - 1)]

    f = open(args.output, 'w')
    f.write('{0} {1}\n'.format(args.dim[0], args.dim[1]))
    f.close()

