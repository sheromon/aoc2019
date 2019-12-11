import numpy as np
import matplotlib.pyplot as plt


def problem11a():
    file_name = 'problem11.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    robot = Robot(program)
    robot.run()


def problem11b():
    file_name = 'problem11.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    robot = Robot(program)
    robot.hull[(0, 0)] = 1  # set starting panel to be white
    robot.run()

    coords = np.array(list(robot.hull.keys()))
    min_coords = np.min(coords, axis=0)
    coords -= min_coords
    max_coords = np.max(coords, axis=0)
    img = np.zeros(max_coords + 1, dtype=np.int32)
    for coord, color in robot.hull.items():
        new_coord = np.array(coord) - min_coords
        img[new_coord[0], new_coord[1]] = color
    plt.figure()
    plt.imshow(img.T, origin='lower')
    plt.savefig('problem11b.jpg')


class Robot():

    def __init__(self, program): #, coords, direction):
        # direction 0 = up, 1 = left, 2 = down, 3 = right
        self.coords = np.zeros(2, dtype=np.int32)
        self.direction = 0
        self.hull = dict()
        self.input_list = []  # robot.get_input(hull)
        self.computer = Computer(program, self.input_list)

    def run(self):
        # detect color of curent panel, run program, paint, turn, and step
        # rinse and repeat
        while not self.computer.done:
            color = self.hull.get(tuple(self.coords), 0)
            self.input_list.insert(0, color)
            if len(self.input_list) != 1:
                print("Input list length:", len(self.input_list))
            new_color = self.computer.run()
            if self.computer.done:
                break
            self.hull[tuple(self.coords)] = new_color
            turn_instruction = self.computer.run()
            if self.computer.done:
                break
            self.turn(turn_instruction)
            self.step()
        print(len(self.hull))

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


class Computer():

    def __init__(self, program, input_list):
        self.program = {key: val for key, val in enumerate(program)}
        self.input_list = input_list
        self.pointer = 0
        self.relative_base = 0
        self.done = False

    def parse_instruction(self):
        instruction = self.program[self.pointer]
        modes = []
        num_params = 0
        opcode = instruction % 100
        if opcode in [1, 2, 7, 8]:
            num_params = 3
        elif opcode in [3, 4, 9]:
            num_params = 1
        elif opcode in [5, 6]:
            num_params = 2
        modes = (instruction // 10**np.arange(2, 2+num_params)) % 10
        return opcode, modes, num_params

    def run(self):
        while True:
            opcode, modes, num_params = self.parse_instruction()
            if opcode == 99:
                self.done = True
                return None

            params = [self.program[ind]
                      for ind in range(self.pointer+1, self.pointer+1+num_params)]
            if opcode in [1, 2, 3, 7, 8]:
                modes, last_mode = modes[:-1], modes[-1]
                assert last_mode != 1  # shouldn't be in value mode
                params, pos = params[:-1], params[-1]
                if last_mode == 2:
                    pos += self.relative_base
            updated_params = []
            for (val, mode) in zip(params, modes):
                if mode == 1:
                    updated_params.append(val)
                else:
                    if mode == 0:
                        ind = val
                    elif mode == 2:
                        ind = val + self.relative_base
                    else:
                        raise RuntimeError("Invalid mode %d." % mode)
                    updated_params.append(self.program.get(ind, 0))
            params = updated_params

            if opcode in [1, 2, 7, 8]:
                if opcode == 1:
                    val = np.sum(params)
                elif opcode == 2:
                    val = np.prod(params)
                elif opcode == 7:  # less than
                    val = int(params[0] < params[1])
                elif opcode == 8:  # equals
                    val = int(params[0] == params[1])
                self.program[pos] = val
            elif opcode == 3:  # input
                self.program[pos] = self.input_list.pop()
                # print("Using input {}".format(self.program[pos]))
            elif opcode == 4:  # output
                output_val = params[0]
                # print("Output: {}".format(output_val))
                # stop processing until we have a new input
                self.pointer += (1 + num_params)
                return output_val
            elif opcode in [5, 6]:
                if opcode == 5:  # jump if true
                    condition = params[0]
                elif opcode == 6:  # jump if false
                    condition = not params[0]
                if condition:
                    self.pointer = params[1]
                    continue
            elif opcode == 9:  # adjust relative base
                self.relative_base += params[0]
            else:
                raise RuntimeError("Bad opcode {:d} at position {:d}".format(
                    opcode, self.pointer))
            self.pointer += (1 + num_params)
        raise RuntimeError("Reached end of program without halting.")


if __name__ == '__main__':
    # problem11a()
    problem11b()
