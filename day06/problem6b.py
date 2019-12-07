

def build_map(orbits):
    orbit_map = dict()
    for orbit in orbits:
        center, planet = orbit.split(')')
        orbit_map[planet] = center
    return orbit_map


def count_indirect(key, orbit_map):
    center = orbit_map.get(key)
    if center not in orbit_map:
        return [(center, 0)]
    history = count_indirect(center, orbit_map)
    prev_num_indirect = history[-1][-1]
    return history + [(center, prev_num_indirect + 1)]


def count_transfers(orbit_map):
    you_history = count_indirect('YOU', orbit_map)
    santa_history = count_indirect('SAN', orbit_map)
    common_history = set(you_history) & set(santa_history)
    sorted_history = sorted(common_history, key=lambda pair: pair[-1])
    last_shared_item = sorted_history[-1]
    you_distance = len(you_history) - you_history.index(last_shared_item) - 1
    santa_distance = len(santa_history) - santa_history.index(last_shared_item) - 1
    total_transfers = you_distance + santa_distance
    return total_transfers

def problem6b():
    file_name = 'problem6.txt'
    with open(file_name) as file_obj:
        lines = [line.strip() for line in file_obj]
    orbit_map = build_map(lines)
    return count_transfers(orbit_map)


def test_problem6b():
    with open('test_6b.txt') as file_obj:
        lines = [line.strip() for line in file_obj]
    orbit_map = build_map(lines)
    assert count_transfers(orbit_map) == 4


if __name__ == '__main__':
    test_problem6b()
    print(problem6b())
