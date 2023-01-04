from grid_class import Grid
from mathematical_models.species_model import SpeciesModel

i=1
thr_cost = 200

grid = Grid(path_grid='./data/data_grid_{}.csv'.format(i),path_threshold='./data/data_thr_{}.csv'.format(i))
maker = SpeciesModel(grid=grid, thr_cost=thr_cost)

model, lands, saved = maker.make_model()
model = maker.add_constraints(model, lands, saved)
model = maker.set_objective_function(model, saved)
model.solve()
species_saved = [i for i, x in enumerate(saved.value()) if x]
obj = model.objective_.value()
print("Real model")
print(f"Species saved: {species_saved}")
print(f"Saved {obj} species")

#feasible model
model, lands, saved, slack_feasible = maker.make_feasible_model()
model_feasible = maker.add_constraints_feasible(model, lands, saved, obj, slack_feasible)
model_feasible = maker.add_species_to_save(model_feasible, saved[1])
model_feasible = maker.set_objective_function_feasible(model_feasible, slack_feasible)
model_feasible.solve()
species_saved = [i for i, x in enumerate(saved.value()) if x]
print("Feasible model")
print(f"Species saved: {species_saved}")
print(f"Saved {len(species_saved)} species")

#unfeasible model
model, lands, saved, slack_unfeasible = maker.make_unfeasible_model()
model_unfeasible = maker.add_constraints_unfeasible(model, lands, saved, obj, slack_unfeasible)
model_unfeasible = maker.add_species_to_save(model_unfeasible, saved[1])
model_unfeasible = maker.set_objective_function_unfeasible(model_unfeasible, slack_unfeasible)
model_unfeasible.solve()
species_saved = [i for i, x in enumerate(saved.value()) if x]
print("Unfeasible model")
print(f"Species saved: {species_saved}")
print(f"Saved {len(species_saved)} species")

#relaxed model
model_relaxed, lands, saved, slack_feasible, slack_unfeasible = maker.make_relaxed_model()
model_relaxed = maker.add_species_to_save(model_relaxed, saved[1])
model_relaxed = maker.add_constraints_relaxed(model_relaxed, lands, saved, obj, slack_feasible, slack_unfeasible)
model_relaxed = maker.set_objective_function_relaxed(model_relaxed, slack_feasible, slack_unfeasible)
model_relaxed.solve()
species_saved = [i for i, x in enumerate(saved.value()) if x]
print("Relaxed model")
print(f"Species saved: {species_saved}")
print(f"Saved {len(species_saved)} species")

