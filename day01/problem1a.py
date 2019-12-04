import numpy as np


def calculate_fuel(mass):
    fuel = np.floor(mass / 3) - 2
    return fuel

def test_fuel_calculation():
    input_mass = 12
    result = calculate_fuel(input_mass)
    assert 2 == result, "Incorrect result for %d" % input_mass
    input_mass = 14
    result = calculate_fuel(input_mass)
    assert 2 == result, "Incorrect result for %d" % input_mass
    input_mass = 1969
    result = calculate_fuel(input_mass)
    assert 654 == result, "Incorrect result for %d" % input_mass
    input_mass = 100756
    result = calculate_fuel(input_mass)
    assert 33583 == result, "Incorrect result for %d" % input_mass

def read_input():
    file_name = 'problem1_input.txt'
    return np.loadtxt(file_name, np.float32)

def problem1a():
    return np.sum([calculate_fuel(mass) for mass in read_input()])

if __name__ == '__main__':
    test_fuel_calculation()
    print(problem1a())

