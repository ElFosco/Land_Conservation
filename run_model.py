from grid_class import Grid
from mathematical_models.species_model import SpeciesModel
import numpy as np


data = 15
thr_cost = 100
i=1
to_relax = {}


grid = Grid(path_grid='./data/data_grid_{}.csv'.format(i),path_threshold='./data/data_thr_{}.csv'.format(i))

to_relax[tuple(['specie',0])] = [250]
to_relax[tuple(['specie',2])] = [150,160]
to_relax[tuple(['specie',7])] = [215,225]
to_relax[tuple(['specie',8])] = [80,90]

model = SpeciesModel(grid=grid, thr_cost=thr_cost)
ris, obj = model.solve()
explanation = model.increase_saved_species_mcs(obj)
print(explanation)

