import numpy as np


class Computer():

    def __init__(self, program, input_list):
        self.program = {key: val for key, val in enumerate(program)}
        self.input_list = input_list
        self.pointer = 0
        self.relative_base = 0
        self.outputs = []
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
                return self.outputs

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
                self.outputs.append(output_val)
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


def problem9a():
    file_name = 'problem9.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    computer = Computer(np.copy(int_array), [1])
    outputs = computer.run()
    return outputs


def problem9b():
    file_name = 'problem9.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    computer = Computer(np.copy(int_array), [2])
    outputs = computer.run()
    return outputs


def test_problem9a():
    test_program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    computer = Computer(np.copy(test_program), [])
    outputs = computer.run()
    assert outputs == test_program

    test_program = [1102,34915192,34915192,7,4,7,99,0]
    computer = Computer(np.copy(test_program), [])
    outputs = computer.run()
    int_str = str(outputs[0])
    assert len(int_str) == 16

    test_program = [104,1125899906842624,99]
    computer = Computer(np.copy(test_program), [])
    outputs = computer.run()
    assert outputs[0] == test_program[1]


if __name__ == '__main__':
    test_problem9a()
    print(problem9a())
    print(problem9b())
