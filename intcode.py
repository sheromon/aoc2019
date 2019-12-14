import logging

import numpy as np
import matplotlib.pyplot as plt

# logging.basicConfig(level=logging.DEBUG)

class Computer():

    def __init__(self, program, input_list=None):
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
            logging.debug("Opcode %d" % opcode)
            logging.debug("Modes %s" % str(modes))
            logging.debug("Params %s" % str(params))
            if opcode in [1, 2, 3, 7, 8]:
                modes, last_mode = modes[:-1], modes[-1]
                assert last_mode != 1  # shouldn't be in value mode
                params, pos = params[:-1], params[-1]
                if last_mode == 2:
                    pos = pos + self.relative_base
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
                    logging.debug("Storing %d + %d in position %d" %
                                  (params[0], params[1], pos))
                elif opcode == 2:
                    val = np.prod(params)
                    logging.debug("Storing %d * %d in position %d" %
                                  (params[0], params[1], pos))
                elif opcode == 7:  # less than
                    val = int(params[0] < params[1])
                    logging.debug("Storing %d in position %d" % (val, pos))
                elif opcode == 8:  # equals
                    val = int(params[0] == params[1])
                    logging.debug("Storing %d in position %d" % (val, pos))
                self.program[pos] = val
            elif opcode == 3:  # input
                self.program[pos] = self.input_list.pop()
                logging.debug("Storing input %d in position %d" % (self.program[pos], pos))
            elif opcode == 4:  # output
                output_val = int(params[0])
                logging.debug("Output %d" % output_val)
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
                    logging.debug("Jumping to %d" % params[1])
                    continue
            elif opcode == 9:  # adjust relative base
                self.relative_base += params[0]
                logging.debug("Adding %d to relative base" % params[0])
            else:
                raise RuntimeError("Bad opcode {:d} at position {:d}".format(
                    opcode, self.pointer))
            self.pointer += (1 + num_params)
        raise RuntimeError("Reached end of program without halting.")

