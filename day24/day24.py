import numpy as np


def problem24a(input_str=None):
    if input_str is None:
        with open('day24.txt') as file_obj:
            input_str = file_obj.read()
    lines = input_str.split('\n')
    char_array = np.array([list(line) for line in lines if line])
    history = []

    grid_size = char_array.shape[0]
    deltas = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])

    # get full set of x-y coords for each cell
    x, y = np.meshgrid(range(grid_size), range(grid_size))
    coords = np.stack((x.flatten(), y.flatten())).T
    while True:
        history.append(np.copy(char_array))
        next_array = np.copy(char_array)
        for coord in coords:
            current_state = char_array[tuple(coord)]
            adj_coords = coord + deltas
            bad_inds = np.any((adj_coords >= grid_size) | (adj_coords < 0), axis=1)
            adj_coords = adj_coords[~bad_inds]
            vals = np.array([char_array[tuple(xy)] for xy in adj_coords])
            num_bugs = np.sum(vals == '#')
            # living bug dies unless there is only one neighbor
            if current_state == '#' and num_bugs != 1:
                next_array[tuple(coord)] = '.'
            # space becomes infested if one or two neighbors
            elif current_state == '.' and num_bugs in [1, 2]:
                next_array[tuple(coord)] = '#'
        char_array = next_array
        # check if current state is the same as a past state
        if any([np.all(char_array == past_array) for past_array in history]):
            break
    return calc_biodiversity(char_array)


def calc_biodiversity(char_array):
    inds = np.where(char_array.reshape(-1) == '#')[0]
    return np.sum(2**inds)


def print_map(char_array):
    lines = [''.join(list(row)) for row in char_array]
    print('\n'.join(lines))


def test_problem24a():
    test_input = [
        '....#',
        '#..#.',
        '#..##',
        '..#..',
        '#....',
    ]
    result = problem24a('\n'.join(test_input))
    assert result == 2129920


if __name__ == '__main__':
    test_problem24a()
    print(problem24a())
