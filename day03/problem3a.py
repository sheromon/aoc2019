import numpy as np


def parse_path(path):
    directions = []
    ints = []
    for instruction in path.split(','):
        directions.append(instruction[0])
        ints.append(int(instruction[1:]))
    return directions, ints


def get_new_cells(coords, dir, val):
    cells = []
    if dir in 'RU':
        step = 1
    else:
        step = -1
    if dir in 'RL':
        coord_idx = 0
    else:
        coord_idx = 1
    for _ in range(val):
        coords[coord_idx] += step
        cells.append(tuple(coords))
    return set(cells)


def calculate_distance(wire1, wire2):
    dirs1, ints1 = parse_path(wire1)
    dirs2, ints2 = parse_path(wire2)
    cells_hit = [set(), set()]

    for iwire, (dirs, ints) in enumerate([(dirs1, ints1), (dirs2, ints2)]):
        coords = [0, 0]
        for dir, val in zip(dirs, ints):
            new_cells = get_new_cells(coords, dir, val)
            cells_hit[iwire] = cells_hit[iwire] | new_cells

    crossings = np.array(list(cells_hit[0] & cells_hit[1]))
    distances = np.sum(np.abs(crossings), axis=1)

    return np.min(distances)


def test_3a():
    path1 = 'R8,U5,L5,D3'
    path2 = 'U7,R6,D4,L4'
    result = calculate_distance(path1, path2)
    assert 6 == result, "Incorrect result for {}".format(path1)

    path1 = 'R75,D30,R83,U83,L12,D49,R71,U7,L72'
    path2 = 'U62,R66,U55,R34,D71,R55,D58,R83'
    result = calculate_distance(path1, path2)
    assert 159 == result, "Incorrect result for {}".format(path1)

    path1 = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51'
    path2 = 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
    result = calculate_distance(path1, path2)
    assert 135 == result, "Incorrect result for {}".format(path1)


def read_input():
    file_name = 'problem3.txt'
    with open(file_name) as file_obj:
        lines = [line.strip() for line in file_obj]
    return lines[:2]


def problem3a():
    wire_paths = read_input()
    return calculate_distance(*wire_paths)


if __name__ == '__main__':
    test_3a()
    print(problem3a())
