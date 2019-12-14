import logging

import numpy as np
import matplotlib.pyplot as plt

from intcode import Computer


def problem11a():
    file_name = 'day11/problem11.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    robot = Robot(program)
    robot.run()
    print(len(robot.hull))


def problem11b():
    file_name = 'day11/problem11.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    robot = Robot(program)
    robot.hull[(0, 0)] = 1  # set starting panel to be white
    robot.run()
    robot.show_hull()


class Robot():

    def __init__(self, program):
        # direction 0 = up, 1 = left, 2 = down, 3 = right
        self.coords = np.zeros(2, dtype=np.int32)
        self.direction = 0
        self.hull = dict()
        self.input_list = []
        self.computer = Computer(program, self.input_list)

    def run(self):
        # detect color of curent panel, run program, paint, turn, and step
        # rinse and repeat
        while not self.computer.done:
            color = self.hull.get(tuple(self.coords), 0)
            self.input_list.insert(0, color)
            if len(self.input_list) != 1:
                logging.warning("Input list length: %d", len(self.input_list))
            new_color = self.computer.run()
            if self.computer.done:
                break
            self.hull[tuple(self.coords)] = new_color
            turn_instruction = self.computer.run()
            if self.computer.done:
                break
            self.turn(turn_instruction)
            self.step()

    def turn(self, val):
        if val == 0:  # turn left
            self.direction = (self.direction + 1) % 4
        elif val == 1:  # turn right
            self.direction = (self.direction - 1) % 4
        else:
            raise ValueError("Turn value is {}.".format(val))

    def step(self):
        if self.direction == 0:
            self.coords[1] += 1
        elif self.direction == 1:
            self.coords[0] -= 1
        elif self.direction == 2:
            self.coords[1] -= 1
        elif self.direction == 3:
            self.coords[0] += 1
        else:
            raise RuntimeError("Bad direction {}.".format(self.direction))

    def show_hull(self):
        coords = np.array(list(self.hull.keys()))
        min_coords = np.min(coords, axis=0)
        coords -= min_coords
        max_coords = np.max(coords, axis=0)
        img = np.zeros(max_coords + 1, dtype=np.int32)
        for coord, color in self.hull.items():
            new_coord = np.array(coord) - min_coords
            img[new_coord[0], new_coord[1]] = color
        plt.imshow(img.T, origin='lower')
        plt.savefig('problem11b.jpg')


if __name__ == '__main__':
    problem11a()
    problem11b()
