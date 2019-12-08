import numpy as np


def get_pixels(int_list, width, height):
    pixels = np.array(int_list)
    pixels = np.reshape(pixels, [-1, height, width])
    return pixels


def problem8a():
    file_name = 'problem8.txt'
    with open(file_name) as file_obj:
        int_str = file_obj.readline().strip()
    int_list = [int(char) for char in int_str]
    pixels = get_pixels(int_list, 25, 6)
    num_zeros = np.sum(np.sum(pixels == 0, axis=2), axis=1)
    layer_ind = np.argmin(num_zeros)
    num_ones = np.sum(pixels[layer_ind] == 1)
    num_twos = np.sum(pixels[layer_ind] == 2)
    return num_ones * num_twos


def test_problem8a():
    test_input = [int(char) for char in '123456789012']
    pixels = get_pixels(test_input, 3, 2)
    print(pixels)


if __name__ == '__main__':
    test_problem8a()
    print(problem8a())
