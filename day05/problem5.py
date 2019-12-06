import numpy as np


def parse_instruction(instruction):
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


def run_program(int_array, input_val):
    pointer = 0
    outputs = []
    while True:
        opcode, modes, num_params = parse_instruction(int_array[pointer])
        if opcode == 99:
            return outputs

        params = int_array[pointer+1:pointer+1+num_params]
        if opcode in [1, 2, 3, 7, 8]:
            modes, last_mode = modes[:-1], modes[-1]
            assert last_mode == 0  # should always be in position mode
            params, pos = params[:-1], params[-1]
        params = [val if mode else int_array[val]
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
            int_array[pos] = val
        elif opcode == 3:  # input
            int_array[pos] = input_val
        elif opcode == 4:  # output
            output_val = params[0]
            print("Output: {}".format(output_val))
            if output_val != 0:
                return output_val
            outputs.append(output_val)
        elif opcode in [5, 6]:
            if opcode == 5:  # jump if true
                condition = params[0]
            elif opcode == 6:  # jump if false
                condition = not params[0]
            if condition:
                pointer = params[1]
                continue
        else:
            raise RuntimeError("Bad opcode {:d} at position {:d}".format(
                opcode, pointer))
        pointer += (1 + num_params)
    return None


def problem5a():
    file_name = 'problem5.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    return run_program(int_array, 1)


def problem5b():
    file_name = 'problem5.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    return run_program(int_array, 5)


if __name__ == '__main__':
    print(problem5a())
    print(problem5b())
