import random

from GridClass import Grid
from utility import generate_random_example
import matplotlib.pyplot as plt

animals=15
for i in range(15):
    grid = generate_random_example(width=10, height=10, initial_cost=3, animals=animals, range_population=range(2, 5),
                                   set_population=[100, 150, 200], set_threshold=[0.3, 0.5, 0.7], cities=random.randrange(1, 2), max_size_cities=4,
                                   lakes=random.randrange(2, 4), max_radius_lake=3, forests=random.randrange(4, 6),
                                   max_radius_forest=7)
    df_grid,df_threshold = grid.convert_into_dfs()
    df_grid.to_csv('./data/data_grid_{}.csv'.format(i))
    df_threshold.to_csv('./data/data_thr_{}.csv'.format(i))
