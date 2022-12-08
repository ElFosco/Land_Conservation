from grid_class import Grid
from mathematical_models.fragmentation_model import FragmentationModel
from mathematical_models.species_model import SpeciesModel

data = 15

for i in range(data):
    grid = Grid(path_grid='./data/data_grid_{}.csv'.format(i),path_threshold='./data/data_thr_{}.csv'.format(i))
    model = SpeciesModel(grid=grid, thr_cost=100)
    result, objective = model.solve()
    print(result)
    print("{} species protected".format(objective))
