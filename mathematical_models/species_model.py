from mathematical_models.base_model import BaseModel


class SpeciesModel(BaseModel):

    def __init__(self, grid, thr_cost):
        super().__init__(grid)
        self.model += (sum((self.lands[i, j] * self.grid.grid_cost[i, j])
                           for i in range(self.height) for j in range(self.width)) <= thr_cost)

    def set_objective_function(self):
        obj_fun = sum(self.saved[i] for i in range(self.grid.animals))
        self.model.maximize(obj_fun)
