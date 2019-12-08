from itertools import permutations

import numpy as np


class Computer():

    def __init__(self, program, input_list):
        self.program = program
        self.input_list = input_list
        self.pointer = 0
        self.output_val = None
        self.done = False

    def parse_instruction(self):
        instruction = self.program[self.pointer]
        modes = []
        num_params = 0
        opcode = instruction % 100
        if opcode in [1, 2, 7, 8]:
            num_params = 3
        elif opcode in [3, 4]:
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
                return self.output_val

            params = self.program[self.pointer+1:self.pointer+1+num_params]
            if opcode in [1, 2, 3, 7, 8]:
                modes, last_mode = modes[:-1], modes[-1]
                assert last_mode == 0  # should always be in position mode
                params, pos = params[:-1], params[-1]
            params = [val if mode else self.program[val]
                    for (val, mode) in zip(params, modes)]

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
                self.output_val = params[0]
                # print("Output: {}".format(self.output_val))
                self.pointer += (1 + num_params)
                return self.output_val
            elif opcode in [5, 6]:
                if opcode == 5:  # jump if true
                    condition = params[0]
                elif opcode == 6:  # jump if false
                    condition = not params[0]
                if condition:
                    self.pointer = params[1]
                    continue
            else:
                raise RuntimeError("Bad opcode {:d} at position {:d}".format(
                    opcode, self.pointer))
            self.pointer += (1 + num_params)
        raise RuntimeError("Reached end of program without halting.")


def check_sequence(program):
    perms = permutations(range(5, 10))
    best_perm = None
    max_output = 0
    for sequence in perms:
        input_val = 0
        computers = {
            'A': Computer(np.copy(program), [input_val, sequence[0]]),
            'B': Computer(np.copy(program), [sequence[1]]),
            'C': Computer(np.copy(program), [sequence[2]]),
            'D': Computer(np.copy(program), [sequence[3]]),
            'E': Computer(np.copy(program), [sequence[4]]),
        }
        routing = {
            'A': 'B',
            'B': 'C',
            'C': 'D',
            'D': 'E',
            'E': 'A',
        }
        amp = 'A'
        while not all([comp.done for comp in computers.values()]):
            output = computers[amp].run()
            next_amp = routing[amp]
            computers[next_amp].input_list.insert(0, output)
            amp = next_amp
        output = computers['E'].output_val

        if output > max_output:
            best_perm = sequence
            max_output = output
    return max_output, best_perm


def problem7b():
    file_name = 'problem7.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    return check_sequence(int_array)[0]


def test_problem7b():
    test_program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
                    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    results = check_sequence(test_program)
    test_program = [
        3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
        -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
        53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
    results = check_sequence(test_program)


if __name__ == '__main__':
    # test_problem7b()
    print(problem7b())
