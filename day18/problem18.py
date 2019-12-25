import copy
import logging

import numpy as np


# logging.basicConfig(level=logging.DEBUG)
ENTRANCE = '@'
WALL = '#'
EMPTY = '.'
DELTAS = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])


def problem18a(map_str=None):
    if map_str is None:
        file_name = 'day18.txt'
        with open(file_name) as file_obj:
            map_str = file_obj.read()

    print(map_str)
    lines = map_str.split('\n')
    char_array = np.array([list(line) for line in lines if line])

    # find the entrance, then replace it with the empty symbol to make
    # things simpler
    start_xy = np.concatenate(np.where(char_array == ENTRANCE))
    special_inds = np.stack(
        np.where((char_array != ENTRANCE) & \
                 (char_array != WALL) & \
                 (char_array != EMPTY))).T
    char_array[tuple(start_xy)] = EMPTY

    # find the keys
    all_keys = set()
    for ind in special_inds:
        char = char_array[tuple(ind)]
        if char.islower():
            all_keys.add(char)
    print(all_keys)

    maze = Maze(char_array, all_keys)
    maze.explore(start_xy)
    return maze.min_steps


class Maze():

    def __init__(self, char_array, all_keys):
        self.char_array = char_array
        self.all_keys = all_keys
        self.distances = dict()
        self.history = []
        self.min_steps = np.inf

    def get_next_coords(self, xy, prev_xy, keys):
        # get all adjacent cells
        deltas = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        next_coords = xy + deltas
        # weed out cells that are walls
        vals = np.array([self.char_array[tuple(xy)] for xy in next_coords])
        ok_inds = vals != WALL
        next_coords, vals = next_coords[ok_inds], vals[ok_inds]
        # weed out cells that are inaccessible (locked doors) and cells that
        # are where we just came from, unless we're getting a key
        ok_inds = np.ones_like(vals, dtype=np.bool)
        special_inds = np.where(vals != EMPTY)[0]
        for ind, val in enumerate(vals):
            if val.isupper():
                ok_inds[ind] = val.lower() in keys
            elif val == EMPTY and np.all(next_coords[ind] == prev_xy):
                ok_inds[ind] = False
        next_coords, vals = next_coords[ok_inds], vals[ok_inds]
        return next_coords, vals

    def explore(self, xy, prev_xy=np.zeros(2)):
        steps = 0
        keys = set()
        while True:
            next_coords, vals = self.get_next_coords(xy, prev_xy, keys)
            next_states = [(next_xy, val, xy, copy.deepcopy(keys)) 
                           for next_xy, val in zip(next_coords, vals)]
            sorted_keys = tuple(sorted(list(keys)))
            xy_keys = (tuple(xy), sorted_keys)
            prev_steps = self.distances.get(xy_keys, np.inf)
            if steps > prev_steps:
                logging.debug("Resetting due to steps > prev_steps")
                next_states = []
            else:
                self.distances[xy_keys] = steps
            while not next_states:
                if steps == 0:
                    logging.debug("Done exploring!")
                    return
                next_states = self.history.pop()
                steps -= 1
            xy, val, prev_xy, keys = next_states.pop()
            self.history.append(next_states)
            steps += 1
            if val != EMPTY:
                if val.islower():
                    logging.debug("Adding key %s at %d steps", val, steps)
                    keys.add(val)
                    # if we just picked up a key, allow backtracking
                    prev_xy = np.zeros(2)
                    if (keys == self.all_keys) and (steps < self.min_steps):
                        self.min_steps = steps

    def print_map(self):
        lines = [''.join(list(row)) for row in self.char_array]
        print('\n'.join(lines))


def test_problem18a():
    test_input = [
        '#########',
        '#b.A.@.a#',
        '#########',
    ]
    result = problem18a('\n'.join(test_input))
    assert result == 8
    print("Completed first test")

    file_name = 'test_input2.txt'
    with open(file_name) as file_obj:
        test_input = file_obj.read()
    result = problem18a(test_input)
    assert result == 86
    print("Completed second test")


if __name__ == '__main__':
    test_problem18a()
    print(problem18a())
