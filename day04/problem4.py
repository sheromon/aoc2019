

def check_digits_a(int_str):
    if len(int_str) < 6:
        raise ValueError("Input length is %d but must be 6." % len(int_str))
    # verify that digits are non-decreasing
    if sorted(int_str) != list(int_str):
        return False
    # verify that two consective digits are the same
    for ind in range(len(int_str) - 1):
        if int_str[ind] == int_str[ind + 1]:
            return True
    return False


def check_digits_b(int_str):
    if len(int_str) < 6:
        raise ValueError("Input length is %d but must be 6." % len(int_str))
    # verify that digits are non-decreasing
    if sorted(int_str) != list(int_str):
        return False
    # verify that two consective digits are the same
    num_adjacent_copies = 0
    for ind in range(len(int_str) - 1):
        if int_str[ind] == int_str[ind + 1]:
            num_adjacent_copies += 1
        elif num_adjacent_copies == 1:
            return True
        else:
            num_adjacent_copies = 0
    return num_adjacent_copies == 1


def test_4a():
    test_input = '111111'
    result = check_digits_a(test_input)
    assert True == result, "Incorrect result for {}".format(test_input)

    test_input = '223450'
    result = check_digits_a(test_input)
    assert False == result, "Incorrect result for {}".format(test_input)

    test_input = '123789'
    result = check_digits_a(test_input)
    assert False == result, "Incorrect result for {}".format(test_input)


def problem4a():
    # puzzle input: 197487-673251
    num_valid = 0
    for val in range(197487, 673251 + 1):
        int_str = str(val)
        num_valid += int(check_digits_a(int_str))
    return num_valid


def test_4b():
    test_input = '112233'
    result = check_digits_b(test_input)
    assert True == result, "Incorrect result for {}".format(test_input)

    test_input = '123444'
    result = check_digits_b(test_input)
    assert False == result, "Incorrect result for {}".format(test_input)

    test_input = '111122'
    result = check_digits_b(test_input)
    assert True == result, "Incorrect result for {}".format(test_input)


def problem4b():
    # puzzle input: 197487-673251
    num_valid = 0
    for val in range(197487, 673251 + 1):
        int_str = str(val)
        num_valid += int(check_digits_b(int_str))
    return num_valid


if __name__ == '__main__':
    test_4a()
    print(problem4a())
    test_4b()
    print(problem4b())
