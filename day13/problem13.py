import time

import numpy as np
import matplotlib.pyplot as plt

from intcode import Computer

EMPTY, WALL, BLOCK, PADDLE, BALL = range(5)


def problem13a():
    file_name = 'day13/problem13.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')

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
    print("Image size:", img_size)
    print("Number of pixels:", len(vals))
    inds = np.ravel_multi_index(tuple(coords.T), img_size)
    img = np.zeros(np.prod(img_size), dtype=np.int32)
    img[inds] = vals
    img = np.reshape(img, img_size)

    print("Initial number of blocks:", np.sum(img == BLOCK))


def make_image(computer, img_size):
    output_list = []
    while not computer.done:
        output_list.append(computer.run())
        if len(output_list) == 3 * np.prod(img_size):
            break

    output_array = np.array(output_list).reshape([-1, 3])
    coords, vals = output_array[:, :2], output_array[:, 2]
    inds = np.ravel_multi_index(tuple(coords.T), img_size)
    img = np.zeros(np.prod(img_size), dtype=np.int32)
    img[inds] = vals
    img = np.reshape(img, img_size)
    return img


def problem13b():
    file_name = 'day13/problem13.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    program[0] = 2  # play for free?

    img_size = (37, 23)
    plt.ion()
    fig = plt.figure()

    joystick = 0  # start in neutral
    input_list = [joystick]
    computer = Computer(program, input_list)
    img = make_image(computer, img_size)
    mpl_img = plt.imshow(img.T)
    plt.axis('off')
    fig.canvas.draw()

    output_list = 3 * [None]
    ball_prev = np.concatenate(np.where(img == BALL))
    while not computer.done:
        for ind in range(3):
            output_list[ind] = computer.run()
        if computer.done:
            break
        if np.all(np.array(output_list[:2]) == np.array([-1, 0])):
            score = output_list[2]
            print("Score:", score)
            continue
        img[output_list[0], output_list[1]] = output_list[2]
        if output_list[2] == BALL:
            mpl_img.set_data(img.T)
            fig.canvas.draw()
            time.sleep(0.02)

            ball_curr = np.array(output_list[:2])
            velocity = ball_curr - ball_prev
            paddle_curr = np.concatenate(np.where(img == PADDLE))
            if velocity[1] == 1:  # ball is falling
                delta = paddle_curr - ball_curr
                ball_x_dest = ball_curr[0] + delta[1] * velocity[0]
                joystick = ball_x_dest - paddle_curr[0] - velocity[0]
            else:
                joystick = ball_curr[0] + velocity[0] - paddle_curr[0]
            joystick = max(min(joystick,  1), -1)
            input_list.append(joystick)
            ball_prev = ball_curr


if __name__ == '__main__':
    problem13a()
    problem13b()
