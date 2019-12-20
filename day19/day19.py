import numpy as np

from intcode import Computer


def problem19a():
    file_name = 'day19/day19.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    map_size = 50
    drone = Drone(program, map_size)
    for x in range(map_size):
        for y in range(map_size):
            drone.update_position(x, y)
    drone.print_map()
    print(np.sum(drone.map))


class Drone():

    def __init__(self, program, map_size):
        self._program = program
        self.input_list = []
        # initialize map values to -1 to indicate unexplored
        self.map = -1 * np.ones((map_size, map_size), dtype=np.int8)

    def update_position(self, x, y):
        self.input_list += [y, x]
        # didn't think I'd need to reset the program every time, but it didn't
        # work otherwise
        self.computer = Computer(np.copy(self._program), self.input_list)
        output = self.computer.run()
        self.map[y, x] = output
        return output

    def print_map(self):
        display_chars = np.array(['.', '#'])
        char_array = display_chars[self.map]
        lines = [''.join(list(row)) for row in char_array]
        print('\n'.join(lines))


if __name__ == '__main__':
    problem19a()
