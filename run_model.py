from GridClass import Grid
from Model import ModelLandConservation

data = 15

for i in range(data):
    grid = Grid(path_grid='./data/data_grid_{}.csv'.format(i),path_threshold='./data/data_thr_{}.csv'.format(i))
    model = ModelLandConservation(grid=grid, thr_cost=100)
    result, objective = model.solve()
    print(result)
    print("{} species protected".format(objective))
