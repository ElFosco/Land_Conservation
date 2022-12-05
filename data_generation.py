import random

from utility import generate_random_example
import matplotlib.pyplot as plt

animals=15
for i in range(15):
    grid = generate_random_example(width=10, height=10, initial_cost=3, animals=animals, range_population=range(1, 5),
                                   set_population=[100, 150, 200], cities=random.randrange(1, 2), max_size_cities=4,
                                   lakes=random.randrange(2, 4), max_radius_lake=4, forests=random.randrange(4, 6),
                                   max_radius_forest=6)
    df = grid.convert_into_df()
    df.to_csv('./data/data_{}.csv'.format(i))