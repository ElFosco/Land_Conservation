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
        return self.lands.value(), self.model.objective_.value(), self.saved.value()


    def make_constraint(self,keyword, threeshold):
        if keyword[0] == 'specie':
            animal = keyword[1]
            expr = (self.saved[animal] * threeshold) <= \
                    sum(self.lands * self.grid.grid_species[animal])
        if keyword[0] == 'cost':
            expr = (sum(self.lands * self.grid.grid_cost) <= threeshold)
        return expr

    def increase_saved_species_xplain(self, obj_fun, to_relax):
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

    def set_constraints_slack(self,obj_fun, model_slack):
        model_slack += sum(self.saved[i] for i in range(self.grid.animals)) == obj_fun
        self.slack = intvar(0, 100, shape=self.grid.animals + 1, name="slack")
        for specie in range(self.grid.animals):
            model_slack += self.make_constraint(['specie', specie], self.grid.species_threshold[specie] - self.slack[specie])
        model_slack += self.make_constraint(['cost'], self.thr_cost + self.slack[-1])
        return model_slack


    def set_obj_function_mcs(self, model_slack_mcs):
        self.flag_slacks = boolvar(shape=len(self.slack) + 1, name="flags_slack")
        for specie in range(self.grid.animals):
            model_slack_mcs += (self.flag_slacks[specie] == (self.slack[specie] > 0))
        model_slack_mcs += (self.flag_slacks[-1] == (self.slack[-1] > 0))
        obj_fun = 1000*sum(self.flag_slacks) + sum(self.slack)
        model_slack_mcs.minimize(obj_fun)
        return model_slack_mcs

    def set_obj_function_mus(self, model_slack_mus):
        obj_fun = 1000 * max(self.slack) + sum(self.slack)
        model_slack_mus.minimize(obj_fun)
        return model_slack_mus


    def increase_saved_species_mcs(self,obj_fun):
        model_slack_mcs = Model()
        model_slack_mcs = self.set_constraints_slack(obj_fun+1,model_slack_mcs)
        model_slack_mcs = self.set_obj_function_mcs(model_slack_mcs)
        model_slack_mcs.solve()
        return self.slack.value()

    def increase_saved_species_mus(self,obj_fun):
        model_slack_mus = Model()
        model_slack_mus = self.set_constraints_slack(obj_fun + 1, model_slack_mus)
        model_slack_mus = self.set_obj_function_mus(model_slack_mus)
        model_slack_mus.solve()
        return self.slack.value()

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


    def generate_slack_model(self, obj_fun):
        model_slack = Model()
        self.slack_unfeasible = intvar(0, 100, shape=self.grid.animals + 1, name="slack_unfeasible")
        self.slack_feasible = intvar(-100,100, name="slack_feasible")
        model_slack += sum(self.saved[i] for i in range(self.grid.animals)) == (obj_fun - self.slack_feasible)
        for specie in range(self.grid.animals):
            model_slack += self.make_constraint(['specie', specie], self.grid.species_threshold[specie] - self.slack_unfeasible[specie])
        model_slack += self.make_constraint(['cost'], self.thr_cost + self.slack_unfeasible[-1])
        return model_slack

    def set_objective_function_slack_model(self, model):
        model_feasible = model
        model_unfeasible = model
        model_feasible += (sum(self.slack_unfeasible for i in range(self.grid.animals + 1)) == 0)
        model_unfeasible += (self.slack_feasible == 0)

        #unfeasible
        self.flag_slacks = boolvar(shape=self.grid.animals + 1, name="flags_slack")
        for specie in range(self.grid.animals):
            model_unfeasible += (self.flag_slacks[specie] == (self.slack_unfeasible[specie] > 0))
        model_unfeasible += (self.flag_slacks[-1] == (self.slack_unfeasible[-1] > 0))
        obj_fun = 1000 * sum(self.flag_slacks) + sum(self.slack_unfeasible)
        model_unfeasible.minimize(obj_fun)

        #feasible
        obj_fun = self.slack_feasible
        model_feasible += (self.saved[1] == True)
        model_feasible.minimize(obj_fun)

        return model_feasible, model_unfeasible



    def set_constraint_save_specie(self, model, index):
        model += (self.saved[index] == True)
        return model

    def solve_model_feasible(self,model_feasible):
        model_feasible.solve()
        print(sum(self.saved.value()))
        return self.lands.value(), self.model.objective_.value(), self.saved.value()

