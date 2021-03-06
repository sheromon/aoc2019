import numpy as np
import matplotlib.pyplot as plt

from intcode import Computer

# if origin is 31, 31, oxygen is at 15, 19

def problem15a():
    file_name = 'problem15.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    plt.ion()
    droid = Droid(program, 60)
    while not droid.computer.done:
        directions, vals = droid.get_next_directions()
        if np.all(vals == droid.map_codes['empty']):
            droid.retrace()
            continue
        for direction in directions:
            droid.send_command(direction)
            output = droid.computer.run()
            if output is None:
                print("Program completed")
            droid.update(direction, output)
            if output == 1:
                droid.display_map()
                break
            if output == 2:
                print("Found oxygen!")
                print("Oxygen is at", droid.coords)
                print("Num steps:", len(droid.history))
                return droid, droid.coords


def problem15b():
    # get to the oxygen!
    droid, oxygen_coords = problem15a()
    droid.reset_map()
    droid.display_map()

    # these are counters for current/max number of steps from oxygen
    num_steps = 0
    max_steps = 0
    # this will help retrace steps after hitting a dead end
    good_directions_history = []

    while not droid.computer.done:
        directions, vals = droid.get_next_directions()
        unexplored_inds = vals == -1
        directions = directions[unexplored_inds]
        good_directions = []
        for direction in directions:
            droid.send_command(direction)
            output = droid.computer.run()
            if output is None:
                print("Program completed")
            droid.update(direction, output)

            if output > 0:
                if output == 2 or np.all(droid.coords == oxygen_coords):
                    print("Found oxygen!")
                    num_steps = 0  # reset counter for steps from oxygen
                good_directions.append(direction)
                droid.retrace()
        if (directions.size == 0) or not good_directions:
            if num_steps > max_steps:
                print("Updated max steps to", num_steps)
                max_steps = num_steps
            good_directions = []
            while not good_directions:
                if num_steps == 0:
                    print("Done exploring!")
                    return
                droid.retrace()
                good_directions = good_directions_history.pop()
                num_steps -= 1
        selected_direction = good_directions.pop()
        droid.send_command(selected_direction)
        output = droid.computer.run()
        droid.update(selected_direction, output)
        droid.display_map()
        good_directions_history.append(good_directions)
        num_steps += 1


class Droid():

    def __init__(self, program, map_size):
        self.input_list = []
        self.computer = Computer(program, self.input_list)
        # initialize map values to -1 to indicate unexplored
        self.map_codes = {
            'droid': -2,
            'unexplored': -1,
            'wall': 0,
            'empty': 1,
            'oxygen': 2,
        }
        self.map = self.map_codes['unexplored'] * np.ones((map_size, map_size), dtype=np.int8)
        self.coords = map_size // 2 + 1 * np.ones(2, dtype=np.int32)
        self.map[self.coords[0], self.coords[1]] = self.map_codes['droid']
        self.fig = plt.figure()  # for displaying map
        self.history = []

    def reset_map(self):
        self.map[:] = self.map_codes['unexplored']
        self.history = []

    def get_retrace_direction(self, prev_direction):
        if prev_direction == 1:
            retrace_direction = 2
        elif prev_direction == 2:
            retrace_direction = 1
        elif prev_direction == 3:
            retrace_direction = 4
        elif prev_direction == 4:
            retrace_direction = 3
        else:
            raise RuntimeError("Invalid previous direction %d" % prev_direction)
        return retrace_direction

    def retrace(self):
        prev_direction = self.history.pop()
        retrace_direction = self.get_retrace_direction(prev_direction)
        self.send_command(retrace_direction)
        output = self.computer.run()
        self.update(retrace_direction, output, retracing=True)

    def send_command(self, direction):
        self.input_list.append(direction)

    def get_next_coords(self, direction):
        if direction == 1:
            next_coords = self.coords + np.array([0, 1])
        elif direction == 2:
            next_coords = self.coords - np.array([0, 1])
        elif direction == 3:
            next_coords = self.coords + np.array([1, 0])
        elif direction == 4:
            next_coords = self.coords - np.array([1, 0])
        return next_coords

    def get_next_directions(self):
        directions = np.arange(1, 5)
        deltas = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
        next_coords = self.coords + deltas
        vals = np.array([self.map[coord[0], coord[1]] for coord in next_coords])
        sort_inds = np.argsort(vals)
        vals = vals[sort_inds]
        directions = directions[sort_inds]
        nonzero_inds = vals != 0
        return directions[nonzero_inds], vals[nonzero_inds]

    def display_map(self):
        plt.cla()
        plt.imshow(self.map.T, origin='lower')
        plt.axis('off')
        self.fig.canvas.draw()

    def update(self, direction, output, retracing=False):
        next_coords = self.get_next_coords(direction)
        self.map[next_coords[0], next_coords[1]] = output
        if output > 0:
            if not retracing:
                self.history.append(direction)
            self.map[self.coords[0], self.coords[1]] = self.map_codes['empty']
            self.coords = next_coords
            self.map[self.coords[0], self.coords[1]] = self.map_codes['droid']


if __name__ == '__main__':
    problem15a()
    problem15b()
