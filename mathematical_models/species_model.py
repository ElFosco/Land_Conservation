from cpmpy import *

class SpeciesModel():

    def __init__(self, grid, thr_cost):
        self.max_species = 0
        self.solutions = []
        self.grid = grid
        self.height = grid.grid_cost.shape[0]
        self.width = grid.grid_cost.shape[1]
        self.model = Model()
        self.thr_cost = thr_cost
        self.lands = boolvar(shape=(self.height, self.width), name="lands")
        self.saved = boolvar(shape=self.grid.animals, name="specie")
        self.model += (sum(self.lands * self.grid.grid_cost) <= self.thr_cost)
        for animal in range(self.grid.animals):
            self.model += (self.saved[animal] * self.grid.species_threshold[animal]) <= \
                          sum(self.lands * self.grid.grid_species[animal])

    def set_objective_function(self):
        obj_fun = sum(self.saved[i] for i in range(self.grid.animals))
        self.model.maximize(obj_fun)

    def solve(self):
        self.set_objective_function()
        self.model.solve()
        self.max_species = self.model.objective_.value()
        return self.lands.value(), self.model.objective_.value()


    def make_constraint(self,keyword,threeshold):
        if keyword[0] == 'specie':
            animal = keyword[1]
            expr = (self.saved[animal] * threeshold) <= \
                    sum(self.lands * self.grid.grid_species[animal])
        if keyword[0] == 'cost':
            expr = (sum(self.lands * self.grid.grid_cost) <= threeshold)
        return expr

    def increase_saved_num_species(self,obj_fun,to_relax):
        obj_fun = obj_fun + 1
        fixed_constraints = []
        fixed_constraints.append(sum(self.saved[i] for i in range(self.grid.animals)) == obj_fun)
        relaxed_constraints = {}
        for keyword in to_relax:
            relaxed_constraints[keyword] = []
            for thr in to_relax[keyword]:
                expr = self.make_constraint(keyword, thr)
                relaxed_constraints[keyword].append(expr)
            if keyword[0] == 'specie':
                thr = self.grid.species_threshold[keyword[1]]
                expr = self.make_constraint(keyword, thr)
                relaxed_constraints[keyword].append(expr)
            if keyword[0] == 'cost':
                expr = self.make_constraint(keyword, self.thr_cost)
                relaxed_constraints[keyword].append(expr)
        for i in range(self.grid.animals):
            if tuple(['specie',i]) not in to_relax:
                expr = self.make_constraint(tuple(['specie',i]), self.grid.species_threshold[i])
                fixed_constraints.append(expr)
        if tuple(['cost']) not in to_relax:
            expr = self.make_constraint(tuple(['cost']), self.thr_cost)
            fixed_constraints.append(expr)
        explanation = self.counter_factual_xplain(relaxed_constraints, fixed_constraints)
        return explanation



    def counter_factual_xplain(self, relaxed_constraints, fixed_constraints):
        '''
            Implementation of CounterFactualXplain
        '''

        self.relaxed_model = Model()
        self.original_constraint = {}
        self.explanation = []
        for fixed_constraint in fixed_constraints:
            self.relaxed_model += fixed_constraint

        for keyword in relaxed_constraints:
            self.relaxed_model += relaxed_constraints[keyword][0]
            self.original_constraint[keyword] = relaxed_constraints[keyword][-1]

        if not self.relaxed_model.solve():
            print("The constraints are not too much relaxed")
            return []

        for keyword in relaxed_constraints:
            for constraint in relaxed_constraints[keyword]:
                temp_relax_model = self.relaxed_model
                temp_relax_model += constraint
                if temp_relax_model.solve():
                    self.relaxed_model += constraint
                    previous_constraint = constraint
                else:
                    constraint = previous_constraint
                    break
            if hash(constraint) != hash(self.original_constraint[keyword]):
                if constraint not in self.explanation:
                    self.explanation.append(constraint)
        return self.explanation



    def storing(self):
        self.solutions.append(self.lands.value())

    def solve_all(self):
        self.set_objective_function()
        self.model.solveAll(display=self.storing)
        return self.solutions, self.model.objective_.value()
