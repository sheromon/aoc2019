import numpy as np


def problem10b():
    file_name = 'problem10.txt'
    with open(file_name) as file_obj:
        input_array = [[char for char in row.strip()] for row in file_obj]
    asteroid_map = np.array(input_array)
    return get_vaporized_order(asteroid_map, zapped_number=200)


def get_max_visible(asteroid_map):
    x, y = np.where(asteroid_map == '#')
    coords = np.stack([x, y]).T
    total_num_asteroids = len(coords)
    max_visible = 0
    rel_coords_for_max = None
    coord_for_max = None
    for irow, coord in enumerate(coords):
        rel_coords = coords - coord
        rel_coords = rel_coords[np.logical_not(np.all(rel_coords == 0, axis=1))]
        normed_coords = rel_coords / np.linalg.norm(rel_coords, axis=1).reshape([-1, 1])
        normed_coords = np.around(normed_coords, 7)
        num_unique = np.unique(normed_coords, axis=0).shape[0]
        if num_unique > max_visible:
            max_visible = num_unique
            coord_for_max = coord
            rel_coords_for_max = rel_coords
    return max_visible, coord_for_max, rel_coords_for_max


def get_vaporized_order(asteroid_map, zapped_number):
    max_visible, coord, rel_coords = get_max_visible(asteroid_map)
    dist = np.linalg.norm(rel_coords, axis=1)
    angle = (np.pi - np.arctan2(rel_coords[:, 1], rel_coords[:, 0])) / np.pi * 180
    angle = np.around(angle, 7)
    angle_bins = max_visible * [[]]
    for iangle,  u_angle in enumerate(np.unique(angle)):
        match_inds = angle == u_angle
        coord_dist = zip(rel_coords[match_inds], dist[match_inds])
        angle_bins[iangle] = sorted(coord_dist, key=lambda tup: tup[1])[::-1]

    zapped = []
    while len(zapped) < zapped_number:
        for entry in angle_bins:
            if entry:
                zapped.append(entry.pop())
            if len(zapped) == 200:
                break
    last_zapped_coord = zapped[-1][0] + coord
    return 100 * last_zapped_coord[0] + last_zapped_coord[1]


if __name__ == '__main__':
    print(problem10b())
