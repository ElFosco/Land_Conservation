from cpmpy import *


class ModelLandConservation:
    def __init__(self, grid, thr_cost):
        self.grid = grid
        self.height = grid.grid_cost.shape[0]
        self.width = grid.grid_cost.shape[1]
        self.thr_cost = thr_cost
        self.model = Model()
        self.lands = intvar(0, 1, shape=(self.height, self.width), name="lands")
        self.saved = intvar(0, 1, shape=self.grid.animals, name="specie")

        for animal in range(self.grid.animals):
            self.model += (self.saved[animal] * self.grid.species_threshold[animal]) <= \
                          sum(self.lands[i, j] * self.grid.grid_species[animal, i, j]
                          for i in range(self.height) for j in range(self.width))

        self.model += (sum((self.lands[i, j] * self.grid.grid_cost[i, j])
                                            for i in range(self.height) for j in range(self.width)) <= thr_cost)




    def set_objective_function(self,type):
        obj_fun = sum(self.saved[i] for i in range(self.grid.animals))
        self.model.maximize(obj_fun)

    def solve(self, type=0):
        self.set_objective_function(type)
        self.model.solve()
        return self.lands.value(), self.model.objective_.value()


