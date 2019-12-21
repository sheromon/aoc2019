import copy
import re

import numpy as np
import matplotlib.pyplot as plt


COORDS = ('x', 'y', 'z')


def problem12a(n_steps= 1000, lines=None):
    if lines is None:
        file_name = 'problem12.txt'
        with open(file_name) as file_obj:
            lines = [line.strip() for line in file_obj]
    system = System(lines)
    system.run(n_steps)
    return system.total_energy


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
        for _ in range(num_steps):
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
        all_pos = np.stack([np.copy(moon.pos) for moon in self.moons])
        all_vel = np.stack([np.copy(moon.vel) for moon in self.moons])
        state = np.concatenate((all_pos, all_vel))
        return state


def test_problem12a():
    test_input = [
        '<x=-1, y=0, z=2>',
        '<x=2, y=-10, z=-7>',
        '<x=4, y=-8, z=8>',
        '<x=3, y=5, z=-1>',
    ]
    result = problem12a(10, test_input)
    assert result == 179


if __name__ == '__main__':
    test_problem12a()
    print(problem12a())
