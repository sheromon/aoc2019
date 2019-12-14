import time

import numpy as np
import matplotlib.pyplot as plt

from intcode import Computer

EMPTY, WALL, BLOCK, PADDLE, BALL = range(5)


def problem13a():
    file_name = 'day13/problem13.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    img = get_initial_image(program)
    print("Initial number of blocks:", np.sum(img == BLOCK))


def get_initial_image(program):
    computer = Computer(program)
    output_list = []
    while not computer.done:
        output_list.append(computer.run())
        if computer.done:
            break
    output_list.pop()  # get rid of None value at the end
    output_array = np.array(output_list).reshape([-1, 3])
    coords, vals = output_array[:, :2], output_array[:, 2]

    max_coords = np.max(coords, axis=0)
    img_size = max_coords + 1
    inds = np.ravel_multi_index(tuple(coords.T), img_size)
    img = np.zeros(np.prod(img_size), dtype=np.int32)
    img[inds] = vals
    img = np.reshape(img, img_size)
    return img


if __name__ == '__main__':
    problem13a()
