import logging

import numpy as np

# logging.basicConfig(level=logging.DEBUG)


def problem20a(char_array=None):
    if char_array is None:
        char_array = read_input('day20.txt')
    maze = Maze(char_array)
    start_coords, prev_coords = maze.gate_coords['AA'][0]
    maze.explore(start_coords, 0, prev_coords)
    return maze.exit_steps


class Maze():

    def __init__(self, char_array):
        self.char_array = char_array
        self.gate_coords = dict()
        self.gate_map = dict()
        self.distances = dict()
        self.find_gates()
        self.history = []

    def find_gates(self):
        np_ord = np.vectorize(ord)
        ascii_array = np_ord(self.char_array)
        letter_inds = (ascii_array >= 65) & (ascii_array <= 90)
        letter_coords = np.stack(np.where(letter_inds)).T
        offsets = np.array([[1, 0], [0, 1]])
        for coords in letter_coords:
            letter1 = self.char_array[coords[0], coords[1]]
            deltas = letter_coords - coords
            for offset in offsets:
                adj_ind = np.where(np.all(deltas == np.array(offset), axis=1))[0]
                if adj_ind.size == 0:
                    continue
                coords2 = coords + offset
                letter2 = self.char_array[coords2[0], coords2[1]]
                gate_name = letter1 + letter2
                adj_coords = coords2 + offset  # this is the gate entrance/exit
                prev_coords = coords2  # record the invalid position next to it
                if self.char_array[adj_coords[0], adj_coords[1]] != '.':
                    adj_coords = coords - offset
                    prev_coords = coords
                    if self.char_array[adj_coords[0], adj_coords[1]] != '.':
                        raise RuntimeError(
                            "Couldn't find empty cell adjacent to gate %s" % gate_name)
                gate_coords = self.gate_coords.get(gate_name, [])
                gate_coords += [(adj_coords, prev_coords)]
                self.gate_coords[gate_name] = gate_coords
                self.gate_map[tuple(gate_coords[-1][0])] = gate_name
                break

    @property
    def exit_steps(self):
        exit_coords = tuple(self.gate_coords['ZZ'][0][0])
        return self.distances.get(exit_coords, np.inf)

    def get_next_coords(self, coords, prev_coords):
        deltas = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        next_coords = coords + deltas
        vals = np.array([self.char_array[coord[0], coord[1]] for coord in next_coords])
        ok_inds = (vals != ' ') & (vals != '#') & \
            ~np.all(next_coords == prev_coords, axis=1)
        return next_coords[ok_inds], vals[ok_inds]

    def explore(self, coords, steps, prev_coords):
        while True:
            next_coords_list, vals = self.get_next_coords(coords, prev_coords)
            next_states = [(next_coord, val, coords)
                           for next_coord, val in zip(next_coords_list, vals)]
            prev_steps = self.distances.get(tuple(coords), np.inf)
            if steps > prev_steps:
                logging.debug("Resetting due to steps > prev_steps")
                next_states = []
            else:
                self.distances[tuple(coords)] = steps
            while not next_states:
                if steps == 0:
                    logging.debug("Done exploring!")
                    return
                next_states = self.history.pop()
                steps -= 1
            next_coords, val, coords = next_states.pop()
            self.history.append(next_states)

            if val != '.':  # use the gate to warp
                gate_name = self.gate_map[tuple(coords)]
                gate_coords, prev_coords = zip(*self.gate_coords[gate_name])
                gate_coords = np.array(gate_coords)
                next_ind = np.argmax(~np.all(gate_coords == coords, axis=1))
                coords = gate_coords[next_ind]
                prev_coords = prev_coords[next_ind]
                logging.debug("Using gate %s" % gate_name)
            else:
                prev_coords = coords
                coords = next_coords

            steps += 1

    def print_map(self):
        lines = [''.join(list(row)) for row in self.char_array]
        print('\n'.join(lines))


def read_input(file_name):
    with open(file_name) as file_obj:
        lines = [np.array(list(line.strip('\n'))) for line in file_obj]
    char_array = np.stack(lines)
    extra_spaces = np.array([char_array.shape[1] * [' ']])
    char_array = np.concatenate((char_array, extra_spaces), axis=0)
    extra_spaces = np.array([char_array.shape[0] * [' ']]).T
    char_array = np.concatenate((char_array, extra_spaces), axis=1)
    return char_array


def test_problem20a():
    char_array = read_input('test_input.txt')
    result = problem20a(char_array)
    assert result == 23
    print("Passed first test")
    char_array = read_input('test_input2.txt')
    result = problem20a(char_array)
    assert result == 58
    print("Passed second test")


if __name__ == '__main__':
    test_problem20a()
    print(problem20a())
