import numpy as np
import matplotlib.pyplot as plt


def get_pixels(int_list, width, height):
    pixels = np.array(int_list)
    pixels = np.reshape(pixels, [-1, height, width])
    return pixels


def collapse_pixels(pixels):
    for layer in range(1, pixels.shape[0]):
        two_inds = pixels[0] == 2
        pixels[0][two_inds] = pixels[layer][two_inds]
    return pixels[0]


def problem8b():
    file_name = 'problem8.txt'
    with open(file_name) as file_obj:
        int_str = file_obj.readline().strip()
    int_list = [int(char) for char in int_str]
    pixels = get_pixels(int_list, 25, 6)
    pixels = collapse_pixels(pixels)

    plt.figure()
    plt.imshow(pixels)
    plt.savefig('problem8.png')
    return pixels


def test_problem8b():
    test_input = [int(char) for char in '0222112222120000']
    pixels = get_pixels(test_input, 2, 2)
    print(collapse_pixels(pixels))


if __name__ == '__main__':
    test_problem8b()
    print(problem8b())
