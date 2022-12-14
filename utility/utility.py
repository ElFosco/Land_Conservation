import itertools

import numpy as np
import random

from grid_class import Grid


def generate_random_example(width, height, initial_cost, animals, range_population, set_population, set_threshold, cities, max_size_cities,
                            lakes, max_radius_lake, forests, max_radius_forest):
    grid = Grid(width,height,initial_cost,animals)
    for animal in range(animals):
        populations = random.choice(list(range_population))
        size_population = 0
        for population in range(populations):
            y = random.randrange(grid.width)
            x = random.randrange(grid.height)
            std = np.random.uniform(0.8, 1.8)
            qty = random.choice(set_population)
            size_population += qty
            grid.add_specie([x, y], std, qty, animal)
        threshold = int(random.choice(set_threshold) * size_population)
        grid.add_specie_threshold(animal,threshold)
    for _ in range(cities):
        width = random.randrange(1,max_size_cities)
        height = random.randrange(1,max_size_cities)
        grid.add_rectangle_constant_cost([random.randrange(0,grid.width-1),random.randrange(grid.height-1)],width,height,15)
    for _ in range(lakes):
        radius = random.randrange(1,max_radius_lake)
        grid.add_circle_constant_cost([random.randrange(0,grid.width-1),random.randrange(grid.height-1)], radius, 5)
    for _ in range(forests):
        radius = random.randrange(1, max_radius_forest)
        grid.add_circle_gaussian_cost([random.randrange(0,grid.width-1),random.randrange(grid.height-1)],
                                      radius,12, np.random.uniform(2,4))
    return grid


def make_coordinates_pair(solution):
    rows = list(range(solution.shape[0]))
    cols = list(range(solution.shape[1]))
    crds = list(itertools.product(rows, cols))
    coordinates_pair = list(itertools.permutations(crds, 2))
    return coordinates_pair

def compute_matrix_distances(solution):
    rows = list(range(solution.shape[0]))
    cols = list(range(solution.shape[1]))
    coordinates_pair = make_coordinates_pair(solution)
    distance_matrix = np.empty((rows, cols, rows, cols))
    for cell_1, cell_2 in coordinates_pair:
        cell_1 = np.asarray(cell_1)
        cell_2 = np.asarray(cell_2)
        if solution[cell_1==True and cell_2==True]:
            distance_matrix[cell_1[0], cell_1[1], cell_2[0], cell_2[1]] = np.linalg.norm(cell_1 - cell_2)
    return distance_matrix





