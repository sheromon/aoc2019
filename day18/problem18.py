import numpy as np


ENTRANCE = '@'
WALL = '#'
EMPTY = '.'
DELTAS = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])

def problem18a(map_str=None):
    if map_str is None:
        file_name = 'day18/problem18.txt'
        with open(file_name) as file_obj:
            map_str = file_obj.read()

    print(map_str)
    lines = map_str.split('\n')
    char_array = np.array([list(line) for line in lines if line])

    coords = np.concatenate(np.where(char_array == ENTRANCE))
    special_inds = np.stack(
        np.where((char_array != ENTRANCE) & \
                 (char_array != WALL) & \
                 (char_array != EMPTY))).T
    keys = {}
    doors = {}
    for ind in special_inds:
        char = char_array[ind[0], ind[1]]
        if char.islower():
            keys[char] = {'coords': ind}
        else:
            doors[char] = {'coords': ind}
    print(coords)
    print(keys)
    print(doors)

    items = find_items(coords, char_array, 0)
    print(items)
    print_map(char_array)
    distances = dict()
    for item in items:
        map_distances(distances, [item['name']], item['coords'], [0], char_array)
    print(distances)
    return


def print_map(char_array):
    lines = [''.join(list(row)) for row in char_array]
    print('\n'.join(lines))


def find_items(coords, char_array, num_steps):
    items = []
    deltas = get_next_directions(coords, char_array)
    for delta in deltas:
        char_array[coords[0], coords[1]] = WALL
        new_coords = coords + delta
        contents = check_pos(new_coords, char_array)
        if contents is not None:
            item = {
                'name': contents,
                'coords': new_coords,
                'num_steps': num_steps + 1,
            }
            items += [item]
        else:
            items += find_items(new_coords, char_array, num_steps + 1)
    return items


def map_distances(distances, names, coords, steps_list, char_array):
    distances[tuple(coords)] = {name: steps for name, steps in zip(names, steps_list)}
    steps_list = [steps + 1 for steps in steps_list]
    deltas = get_next_directions(coords, char_array)
    for delta in deltas:
        char_array[coords[0], coords[1]] = WALL
        new_coords = coords + delta
        contents = check_pos(new_coords, char_array)
        if contents is not None:
            names += contents
            steps_list += [0]
        map_distances(distances, names, new_coords, steps_list, char_array)


def get_next_directions(coords, char_array):
    directions = np.arange(4)
    next_coords = coords + DELTAS
    chars = np.array([char_array[coord[0], coord[1]]
                        for coord in next_coords])
    bad_inds = chars == WALL
    return list(DELTAS[~bad_inds])


def check_pos(coords, char_array):
    current_val = char_array[coords[0], coords[1]]
    if current_val not in [WALL, EMPTY, ENTRANCE]:
        return current_val
    else:
        return None


def test_problem18a():
    test_input = [
        '#########',
        '#b.A.@.a#',
        '#########',
    ]
    result = problem18a('\n'.join(test_input))


if __name__ == '__main__':
    test_problem18a()
