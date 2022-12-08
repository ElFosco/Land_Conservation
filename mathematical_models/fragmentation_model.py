import itertools

import numpy as np
from cpmpy import *

from mathematical_models.base_model import BaseModel


class FragmentationModel(BaseModel):

    def __init__(self, grid, thr_cost, thr_species):
        super(FragmentationModel, self).__init__(grid)
        rows = list(range(self.height))
        cols = list(range(self.width))
        self.crds = list(itertools.product(rows, cols))
        self.coordinates_pair = list(itertools.permutations(self.crds, 2))
        self.distance = np.zeros((self.height, self.width, self.height, self.width))

        for cell_1, cell_2 in self.coordinates_pair:
            cell_1 = np.asarray(cell_1)
            cell_2 = np.asarray(cell_2)
            self.distance[cell_1[0], cell_1[1], cell_2[0], cell_2[1]] = np.linalg.norm(cell_1-cell_2)

        self.closest = intvar(0, 1, shape=(self.height, self.width, self.height, self.width), name="lands")


        self.model += ((sum(self.closest[cell_1[0],cell_1[1],cell_2[0],cell_2[1]] for cell_1 in self.crds) ==
                        self.lands[cell_2[0], cell_2[1]]) for cell_2 in self.crds)

        self.model += (self.closest[cell_1[0], cell_1[1], cell_2[0], cell_2[1] <= self.lands[cell_2[0], cell_2[1]]]
                       for cell_1, cell_2 in self.coordinates_pair)

        self.model += (sum((self.lands[i, j] * self.grid.grid_cost[i, j])
                           for i in range(self.height) for j in range(self.width)) <= thr_cost)

        self.model += (sum(self.saved[i] for i in range(self.grid.animals)) >= thr_species)




    def set_objective_function(self):
        obj_fun = (sum(self.closest[cell_1[0], cell_1[1], cell_2[0], cell_2[1]]*
             self.distance[cell_1[0], cell_1[1], cell_2[0], cell_2[1]] for cell_1, cell_2 in self.coordinates_pair)) \
        / (sum(self.lands[i, j] for i in range(self.height) for j in range(self.width)))
        self.model.minimize(obj_fun)

    def solve(self):
        self.set_objective_function()
        self.model.solve()
        return self.lands.value(), self.model.objective_.value()