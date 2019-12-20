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
    char_map = drone.get_map()
    print(char_map)
    with open('map.txt', 'w') as file_obj:
        file_obj.write(char_map)
    print(np.sum(drone.map))


def problem19b():
    file_name = 'day19/day19.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')

    with open('map.txt') as file_obj:
        lines = [np.array(list(line.strip())) for line in file_obj  if line.strip()]
        char_array = np.stack(lines)
    coords = np.stack(np.where(char_array == '#')).T

    map_size = 5000
    beam_width_array = np.zeros(map_size, dtype=np.int32)
    drone = Drone(program, map_size)
    # update the new map with the info that we got in part a
    drone.map[:char_array.shape[0], :char_array.shape[1]] = char_array == '#'
    for y in range(map_size):
        min_x, max_x = drone.get_min_and_max(y)

    ship_size = 100
    y = 48
    step = map_size - y - ship_size - 1
    while True:
        min_x, max_x = drone.get_min_and_max(y)
        pred_min_x = int(np.ceil(min_x + min_x/y * step))
        pred_max_x = int(np.floor(max_x + max_x/y * step))
        update_region(drone, y + step, pred_min_x, -1)
        update_region(drone, y + step, pred_max_x, +1)

        y += step
        min_x, max_x = drone.get_min_and_max(y)
        pred_min_x = int(np.ceil(min_x + min_x/y * (ship_size - 1)))
        update_region(drone, y + ship_size - 1, pred_min_x, -1)
        bottom_min_x, _ = drone.get_min_and_max(y + ship_size - 1)
        beam_width = max_x - bottom_min_x + 1
        print("Row %d, beam width %d" % (y, beam_width))
        beam_width_array[y] = beam_width
        if beam_width >= ship_size:
            prev_y = np.where(beam_width_array[:y] > 0)[0]
            if len(prev_y):
                prev_y = prev_y[-1]
            else:
                prev_y = 0
            step = int(np.floor((prev_y - y)/2))
            if (step == -1) and beam_width_array[y-1] == ship_size - 1:
                break
        else:
            prev_y = y + 1 + np.argmax(beam_width_array[y+1:] >= ship_size)
            step = int(np.ceil((prev_y - y)/2))

    x = max_x - ship_size + 1
    print(10000 * x + y)


def update_region(drone, y, x, step_sign):
    result = True
    while result:
        result = drone.update_position(x, y)
        x += step_sign


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

    def get_map(self):
        display_chars = np.array(['.', '#', '?'])
        char_array = display_chars[self.map]
        lines = [''.join(list(row)) for row in char_array]
        return '\n'.join(lines)

    def get_min_and_max(self, row_id):
        x_vals = np.where(self.map[row_id] == 1)[0]
        if x_vals.size == 0:
            return 0, 0
        min_x = np.min(x_vals)
        max_x = np.max(x_vals)
        return min_x, max_x


if __name__ == '__main__':
    problem19a()
    problem19b()
