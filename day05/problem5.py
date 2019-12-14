import numpy as np

from intcode import Computer


def problem5a():
    file_name = 'day05/problem5.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    computer = Computer(program, [1])
    output = 0
    while not output:
        output = computer.run()
    return output


def problem5b():
    file_name = 'day05/problem5.txt'
    program = np.loadtxt(file_name, np.int32, delimiter=',')
    computer = Computer(program, [5])
    output = computer.run()
    return output


if __name__ == '__main__':
    print(problem5a())
    print(problem5b())
