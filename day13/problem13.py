import time

import numpy as np
import matplotlib.pyplot as plt

from intcode import Computer

EMPTY, WALL, BLOCK, PADDLE, BALL = range(5)


def problem13a():
    file_name = 'day13/problem13.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    img = get_initial_image(program)

    ball_coords = np.concatenate(np.where(img == BALL))
    ball = Ball(*tuple(ball_coords))

    plt.ion()
    fig = plt.figure()
    mpl_img = plt.imshow(img.T)
    plt.axis('off')

    for _ in range(20):
        ball.step(img)
        mpl_img.set_data(img.T)
        fig.canvas.draw()
        time.sleep(0.5)


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


class Ball():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_dir = 1
        self.y_dir = 1

    def step(self, grid):
        grid[self.x, self.y] = EMPTY
        self.x += self.x_dir
        self.y += self.y_dir
        grid[self.x, self.y] = BALL

        next_x = self.x + self.x_dir
        next_y = self.y + self.y_dir
        if grid[next_x, self.y] != EMPTY:
            self.destroy_if_block(grid, next_x, self.y)
            self.x_dir *= -1
        elif grid[self.x, next_y] != EMPTY:
            self.destroy_if_block(grid, self.x, next_y)
            self.y_dir *= -1
        elif grid[next_x, next_y] != EMPTY:
            self.destroy_if_block(grid, next_x, next_y)
            self.x_dir *= -1
            self.y_dir *= -1

    def destroy_if_block(self, grid, x, y):
        if grid[x, y] == BLOCK:
            grid[x, y] = EMPTY



if __name__ == '__main__':
    problem13a()
