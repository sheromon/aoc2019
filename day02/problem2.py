import copy

import numpy as np

from intcode import Computer


def run_program(int_list):
    comp = Computer(int_list, [])
    comp.run()
    return list(comp.program.values())

def test_computer():
    test_int_list = [1,0,0,0,99]
    result = run_program(test_int_list)
    assert [2,0,0,0,99] == result, "Incorrect result for {}".format(test_int_list)
    test_int_list = [2,3,0,3,99]
    result = run_program(test_int_list)
    assert [2,3,0,6,99] == result, "Incorrect result for {}".format(test_int_list)
    test_int_list = [2,4,4,5,99]
    result = run_program(test_int_list)
    assert [2,4,4,5,99,9801] == result, "Incorrect result for {}".format(test_int_list)
    test_int_list = [1,1,1,4,99,5,6,0,99]
    result = run_program(test_int_list)
    assert [30,1,1,4,2,5,6,0,99] == result, "Incorrect result for {}".format(test_int_list)
    test_int_list = [1,9,10,3,2,3,11,0,99,30,40,50]
    result = run_program(test_int_list)
    assert [3500,9,10,70,2,3,11,0,99,30,40,50] == result, "Incorrect result for {}".format(test_int_list)

def read_input():
    file_name = 'day02/problem2.txt'
    return np.loadtxt(file_name, np.int32, delimiter=',').tolist()

def problem2a():
    int_list = read_input()
    int_list[1] = 12
    int_list[2] = 2
    return run_program(int_list)[0]

def problem2b():
    int_list = read_input()
    for noun in range(100):
        for verb in range(100):
            new_int_list = copy.deepcopy(int_list)
            new_int_list[1] = noun
            new_int_list[2] = verb
            output = run_program(new_int_list)[0]
            if output == 19690720:
                return 100 * noun + verb
    return None


if __name__ == '__main__':
    test_computer()
    print(problem2a())
    print(problem2b())
