

def build_map(orbits):
    orbit_map = dict()
    for orbit in orbits:
        center, planet = orbit.split(')')
        orbit_map[planet] = center
    return orbit_map


def count_indirect(key, orbit_map):
    # since we're doing this to every key in the map, it would be more
    # efficient to store the results as they compute them. this way, we're
    # recounting the same paths multiple times. but it runs fast enough
    # without the optimization, so eh.
    center = orbit_map.get(key)
    if center not in orbit_map:
        return 0
    return count_indirect(center, orbit_map) + 1


def count_orbits(orbit_map):
    num_direct = len(orbit_map)
    num_indirect = 0
    for key in orbit_map:
        num_indirect += count_indirect(key, orbit_map)

    return num_direct + num_indirect


def problem6a():
    file_name = 'problem6.txt'
    with open(file_name) as file_obj:
        lines = [line.strip() for line in file_obj]
    orbit_map = build_map(lines)
    return count_orbits(orbit_map)


def test_problem6a():
    with open('test_input.txt') as file_obj:
        lines = [line.strip() for line in file_obj]
    orbit_map = build_map(lines)
    assert count_indirect('D', orbit_map) == 2
    assert count_indirect('L', orbit_map) == 6
    assert count_orbits(orbit_map) == 42


if __name__ == '__main__':
    test_problem6a()
    print(problem6a())
