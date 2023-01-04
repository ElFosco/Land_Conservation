from cpmpy import *

class SpeciesModel():

    def __init__(self, grid, thr_cost):
        self.max_species = 0
        self.solutions = []
        self.grid = grid
        self.height = grid.grid_cost.shape[0]
        self.width = grid.grid_cost.shape[1]
        self.thr_cost = thr_cost

    def make_model(self):
        model = Model()
        lands = boolvar(shape=(self.height, self.width), name="lands")
        saved = boolvar(shape=self.grid.animals, name="specie")
        return model, lands, saved

    def make_unfeasible_model(self):
        model = Model()
        lands = boolvar(shape=(self.height, self.width), name="lands")
        saved = boolvar(shape=self.grid.animals, name="specie")
        slack_unfeasible = intvar(0, 100, shape=self.grid.animals + 1, name="slack_unfeasible")
        return model, lands, saved, slack_unfeasible

    def make_feasible_model(self):
        model = Model()
        lands = boolvar(shape=(self.height, self.width), name="lands")
        saved = boolvar(shape=self.grid.animals, name="specie")
        slack_feasible = intvar(-100, 100, name="slack_feasible")
        return model, lands, saved, slack_feasible

    def make_relaxed_model(self):
        model = Model()
        lands = boolvar(shape=(self.height, self.width), name="lands")
        saved = boolvar(shape=self.grid.animals, name="specie")
        slack_unfeasible = intvar(0, 100, shape=self.grid.animals + 1, name="slack_unfeasible")
        slack_feasible = intvar(0, 100, name="slack_feasible")
        return model, lands, saved, slack_feasible, slack_unfeasible


    def add_constraints(self, model, lands, saved):
        model += (sum(lands * self.grid.grid_cost) <= self.thr_cost)
        for animal in range(self.grid.animals):
            model += (saved[animal] * self.grid.species_threshold[animal]) <= \
                      sum(lands * self.grid.grid_species[animal])
        return model

    def add_constraints_feasible(self, model, lands, saved, obj, slack_feasible):
        model += (sum(lands * self.grid.grid_cost) <= self.thr_cost)
        model += sum(saved[i] for i in range(self.grid.animals)) == (obj - slack_feasible)
        for animal in range(self.grid.animals):
            model += (saved[animal] * self.grid.species_threshold[animal]) <= \
                      sum(lands * self.grid.grid_species[animal])
        return model

    def add_constraints_unfeasible(self, model, lands, saved, obj, slack_unfeasible):
        model += sum(saved[i] for i in range(self.grid.animals)) == obj
        model += (sum(lands * self.grid.grid_cost) <= self.thr_cost + slack_unfeasible[-1])
        for animal in range(self.grid.animals):
            model += (saved[animal] * (self.grid.species_threshold[animal] - slack_unfeasible[animal])) \
                     <= sum(lands * self.grid.grid_species[animal])
        return model

    def add_constraints_relaxed(self, model, lands, saved, obj, slack_feasible, slack_unfeasible):
        model += sum(saved[i] for i in range(self.grid.animals)) == (obj - slack_feasible)
        model += (sum(lands * self.grid.grid_cost) <= self.thr_cost + slack_unfeasible[-1])
        for animal in range(self.grid.animals):
            model += (saved[animal] * (self.grid.species_threshold[animal] - slack_unfeasible[animal])) \
                     <= sum(lands * self.grid.grid_species[animal])
        return model

    def set_objective_function(self, model, saved):
        obj_fun = sum(saved[i] for i in range(self.grid.animals))
        model.maximize(obj_fun)
        return model

    def set_objective_function_unfeasible(self, model, slack_unfeasible):
        flag_slacks = boolvar(shape=self.grid.animals + 1, name="flags_slack")
        for specie in range(self.grid.animals):
            model += (flag_slacks[specie] == (slack_unfeasible[specie] > 0))
        model += (flag_slacks[-1] == (slack_unfeasible[-1] > 0))
        obj_fun = 1000 * sum(flag_slacks) + sum(slack_unfeasible)
        model.minimize(obj_fun)
        return model

    def set_objective_function_feasible(self, model, slack_feasible):
        obj_fun = slack_feasible
        model.minimize(obj_fun)
        return model

    def set_objective_function_relaxed(self, model, slack_feasible, slack_unfeasible):
        flag_slacks = boolvar(shape=self.grid.animals + 1, name="flags_slack")
        for specie in range(self.grid.animals):
            model += (flag_slacks[specie] == (slack_unfeasible[specie] > 0))
        model += (flag_slacks[-1] == (slack_unfeasible[-1] > 0))
        obj_fun = 100*slack_feasible + ((10 * sum(flag_slacks) + sum(slack_unfeasible)))
        model.minimize(obj_fun)
        return model

    def add_species_to_save(self, model, specie):
        model += (specie == True)
        return model

