from cpmpy import *


class BaseModel:
    def __init__(self, grid):
        self.grid = grid
        self.height = grid.grid_cost.shape[0]
        self.width = grid.grid_cost.shape[1]
        self.model = Model()
        self.lands = intvar(0, 1, shape=(self.height, self.width), name="lands")
        self.saved = intvar(0, 1, shape=self.grid.animals, name="specie")

        for animal in range(self.grid.animals):
            self.model += (self.saved[animal] * self.grid.species_threshold[animal]) <= \
                          sum(self.lands[i, j] * self.grid.grid_species[animal, i, j]
                          for i in range(self.height) for j in range(self.width))




    def set_objective_function(self):
        pass

    def solve(self):
        self.set_objective_function()
        self.model.solve()
        return self.lands.value(), self.model.objective_.value()





