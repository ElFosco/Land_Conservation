import numpy as np
import random

from GridClass import Grid


def generate_random_example(width, height, initial_cost, animals, range_population, set_population, cities, max_size_cities,
                            lakes, max_radius_lake, forests, max_radius_forest):
    grid = Grid(width,height,initial_cost,animals)
    for animal in range(animals):
        populations = random.choice(list(range_population))
        for population in range(populations):
            y = random.randrange(grid.width)
            x = random.randrange(grid.height)
            std = np.random.uniform(0.8, 1.8)
            qty = random.choice(set_population)
            grid.adds_specie([x, y], std, qty, animal)
    for _ in range(cities):
        width = random.randrange(1,max_size_cities)
        height = random.randrange(1,max_size_cities)
        grid.add_rectangle_constant_cost([random.randrange(0,grid.width-1),random.randrange(grid.height-1)],width,height,10)
    for _ in range(lakes):
        radius = random.randrange(1,max_radius_lake)
        grid.add_circle_constant_cost([random.randrange(0,grid.width-1),random.randrange(grid.height-1)], radius, 5)
    for _ in range(forests):
        radius = random.randrange(1, max_radius_forest)
        grid.add_circle_gaussian_cost([random.randrange(0,grid.width-1),random.randrange(grid.height-1)],
                                      radius,10, np.random.uniform(2,4))
    return grid








