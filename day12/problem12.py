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
    return system.get_total_energy()


def problem12b():
    pass


class System():

    def __init__(self, moon_init):
        self.moons = []
        for line in moon_init:
            kwargs = self.parse_line(line)
            self.moons.append(Moon(**kwargs))

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
            self.step()

    def step(self):
        pos_array = np.stack([moon.pos for moon in self.moons])
        for moon in self.moons:
            delta = pos_array - moon.pos
            gravity = np.maximum(np.minimum(delta, 1), -1)
            moon.apply_gravity(np.sum(gravity, axis=0))
        for moon in self.moons:
            moon.apply_velocity()

    def get_total_energy(self):
        return sum([moon.total_energy for moon in self.moons])


class Moon():

    def __init__(self, x, y, z):
        self.pos = np.array([x, y, z], dtype=np.int32)
        self.vel = np.zeros(3, dtype=np.int32)

    def __repr__(self):
        pos_str = ', '.join(
            ['{:s}={:d}'.format(COORDS[ind], self.pos[ind]) for ind in range(3)])
        vel_str = ', '.join(
            ['{:s}={:d}'.format(COORDS[ind], self.vel[ind]) for ind in range(3)])
        display_str = 'pos=<{:s}>, vel={:s}>'.format(pos_str, vel_str)
        return display_str

    def apply_gravity(self, grav):
        self.vel += grav

    def apply_velocity(self):
        self.pos += self.vel

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy

    @property
    def potential_energy(self):
        return np.sum(np.abs(self.pos))

    @property
    def kinetic_energy(self):
        return np.sum(np.abs(self.vel))


def test_problem12a():
    test_input = [
        '<x=-1, y=0, z=2>',
        '<x=2, y=-10, z=-7>',
        '<x=4, y=-8, z=8>',
        '<x=3, y=5, z=-1>',
    ]
    system = System(test_input)
    system.run(10)
    assert system.get_total_energy() == 179


if __name__ == '__main__':
    test_problem12a()
    print(problem12a())
