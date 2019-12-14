import numpy as np

from intcode import Computer


def problem9a():
    file_name = 'day09/problem9.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    computer = Computer(np.copy(int_array), [1])
    output = computer.run()
    return output


def problem9b():
    file_name = 'day09/problem9.txt'
    int_array = np.loadtxt(file_name, np.int32, delimiter=',')
    computer = Computer(np.copy(int_array), [2])
    output = computer.run()
    return output


def test_problem9a():
    test_program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    computer = Computer(np.copy(test_program), [])
    outputs = []
    while not computer.done:
        outputs.append(computer.run())
    assert outputs[:-1] == test_program

    test_program = [1102,34915192,34915192,7,4,7,99,0]
    computer = Computer(np.copy(test_program), [])
    output = computer.run()
    int_str = str(output)
    assert len(int_str) == 16

    test_program = [104,1125899906842624,99]
    computer = Computer(np.copy(test_program), [])
    output = computer.run()
    assert output == test_program[1]


if __name__ == '__main__':
    test_problem9a()
    print(problem9a())
    print(problem9b())
