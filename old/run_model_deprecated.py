from grid_class import Grid
from old.species_model_deprecated import SpeciesModel

data = 15
thr_cost = 200
i=1
to_relax = {}


grid = Grid(path_grid='./data/data_grid_{}.csv'.format(i),path_threshold='./data/data_thr_{}.csv'.format(i))
'''
to_relax[tuple(['specie',0])] = [250]
to_relax[tuple(['specie',2])] = [150,160]
to_relax[tuple(['specie',7])] = [215,225]
to_relax[tuple(['specie',8])] = [80,90]
'''
'''
model = SpeciesModel(grid=grid, thr_cost=thr_cost)
ris, obj = model.solve()
print(f"Saved {obj} species")
explanation = model.increase_saved_species_xplain(obj,to_relax)
explanation = model.increase_saved_species_mus(obj)
print(explanation)
'''

model = SpeciesModel(grid=grid, thr_cost=thr_cost)
ris, obj, saved = model.solve()
species_saved = [i for i, x in enumerate(saved) if x]
print(f"Species saved: {species_saved}")
print(f"Saved {obj} species")


slack_model = model.generate_slack_model(obj)
#slack_model = model.set_constraint_save_specie(slack_model, 5)
feasible_model, unfeasible_model = model.set_objective_function_slack_model(slack_model)
ris, obj, saved = model.solve_model_feasible(feasible_model)
species_saved = [i for i, x in enumerate(saved) if x]
print(f"Species saved: {species_saved}")
print(f"Saved {obj} species")
