import copy
import re

import numpy as np
import matplotlib.pyplot as plt


COORDS = ('x', 'y', 'z')


def problem12a():
    file_name = 'problem12.txt'
    with open(file_name) as file_obj:
        lines = [line.strip() for line in file_obj]
    system = System(lines)
    system.run(1000)
    return system.total_energy


def problem12b(lines=None):
    if lines is None:
        file_name = 'problem12.txt'
        with open(file_name) as file_obj:
            lines = [line.strip() for line in file_obj]
    system = System(lines)
    initial_state = system.get_state()
    # state_history = [initial_state]
    total_steps = 0
    done = False
    report_interval = 1000000
    while not done:
        system.run(1)
        total_steps += 1
        current_state = system.get_state()
        if np.all(current_state == initial_state):
            done = True
            break
        if total_steps % report_interval == 0:
            print('Step %dM' % (total_steps//report_interval))
        # for past_state in state_history:
        #     if np.all(current_state == past_state):
        #         done = True
        #         break
        # state_history.append(current_state)
    return total_steps


class System():

    def __init__(self, moon_init):
        n_moons = len(moon_init)
        self.pos = np.zeros((n_moons, 3), np.int64)
        self.vel = np.zeros((n_moons, 3), np.int64)
        for imoon, line in enumerate(moon_init):
            pos_dict = self.parse_line(line)
            self.pos[imoon, :] = np.array(
                [pos_dict['x'], pos_dict['y'], pos_dict['z']])

    def parse_line(self, line):
        pattern = r'[a-z]=-*\d+'
        matches = re.compile(pattern).findall(line)
        kwargs = dict()
        for match in matches:
            key, val = match.split('=')
            kwargs[key] = int(val)
        assert all([key in kwargs for key in COORDS])
        return kwargs

    def run(self, num_steps):
        for istep in range(num_steps):
            pos1 = self.pos[None, :]
            pos2 = self.pos[:, None]
            delta = pos1 - pos2
            gravity = np.maximum(np.minimum(delta, 1), -1)
            self.apply_gravity(np.sum(gravity, axis=1))
            self.apply_velocity()

    def apply_gravity(self, gravity):
        self.vel += gravity

    def apply_velocity(self):
        self.pos += self.vel

    @property
    def total_energy(self):
        return np.sum(self.potential_energy * self.kinetic_energy)

    @property
    def potential_energy(self):
        return np.sum(np.abs(self.pos), axis=1)

    @property
    def kinetic_energy(self):
        return np.sum(np.abs(self.vel), axis=1)

    def get_state(self):
        return np.concatenate((self.pos, self.vel))


def test_problem12b():
    test_input = [
        '<x=-1, y=0, z=2>',
        '<x=2, y=-10, z=-7>',
        '<x=4, y=-8, z=8>',
        '<x=3, y=5, z=-1>',
    ]
    total_steps = problem12b(test_input)
    assert total_steps == 2772


if __name__ == '__main__':
    test_problem12b()
    print(problem12b())
