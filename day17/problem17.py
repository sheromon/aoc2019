import numpy as np
import matplotlib.pyplot as plt

from intcode import Computer


def problem17a(camera_output=None):
    if camera_output is None:
        file_name = 'day17/problem17.txt'
        program = np.loadtxt(file_name, np.int32, delimiter=',')
        computer = Computer(program)
        camera_output = ''
        while not computer.done:
            output = computer.run()
            if output is not None:
                camera_output += chr(output)
        print(camera_output)

    lines = camera_output.split('\n')
    char_array = np.array([list(line) for line in lines if line])

    intersections = []
    n_rows, n_cols = char_array.shape
    for irow in range(n_rows):
        for icol in range(n_cols):
            if char_array[irow, icol] == '#':
                cross_row = ((irow > 0) and (char_array[irow-1, icol] == '#')) \
                    and ((irow < n_rows-1) and (char_array[irow+1, icol] == '#'))
                cross_col = ((icol > 0) and (char_array[irow, icol-1] == '#')) \
                    and ((icol < n_cols-1) and (char_array[irow, icol+1] == '#'))
                if cross_row and cross_col:
                    coords = (irow, icol)
                    intersections.append(coords)
    intersection_array = np.array(intersections)
    alignment = np.sum(np.prod(intersection_array, axis=1))
    return alignment


def test_problem17a():
    test_input = [
        '..#..........',
        '..#..........',
        '#######...###',
        '#.#...#...#.#',
        '#############',
        '..#...#...#..',
        '..#####...^..',
    ]
    assert problem17a('\n'.join(test_input)) == 76


if __name__ == '__main__':
    test_problem17a()
    print(problem17a())
