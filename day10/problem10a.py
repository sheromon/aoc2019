import numpy as np


def problem10a():
    file_name = 'problem10.txt'
    with open(file_name) as file_obj:
        input_array = [[char for char in row.strip()] for row in file_obj]
    asteroid_map = np.array(input_array)
    return get_max_visible(asteroid_map)


def get_max_visible(asteroid_map):
    x, y = np.where(asteroid_map == '#')
    coords = np.stack([x, y]).T
    total_num_asteroids = len(coords)
    max_visible = 0
    for irow, coord in enumerate(coords):
        rel_coords = coords - coord
        rel_coords = rel_coords[np.logical_not(np.all(rel_coords == 0, axis=1))]
        normed_coords = rel_coords / np.linalg.norm(rel_coords, axis=1).reshape([-1, 1])
        normed_coords = np.around(normed_coords, 7)
        num_unique = np.unique(normed_coords, axis=0).shape[0]
        # print("Visible from ", coord, num_unique)
        if num_unique > max_visible:
            max_visible = num_unique
    return(max_visible)


def test_problem10a():
    input_str = [
        '.#..#',
        '.....',
        '#####',
        '....#',
        '...##',
    ]
    input_array = [[char for char in row] for row in input_str]
    asteroid_map = np.array(input_array)
    assert get_max_visible(asteroid_map) == 8


if __name__ == '__main__':
    test_problem10a()
    print(problem10a())
