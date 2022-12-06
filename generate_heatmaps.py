from matplotlib import pyplot as plt

from GridClass import Grid

data=15

for i in range(data):
    print(i)
    grid = Grid(path='./data/data_{}.csv'.format(i))
    plt.imshow(grid.grid_cost, cmap='hot', interpolation='nearest')
    plt.savefig('visualization/heatmap/data_{}/map_cost.png'.format(i))
    for j in range(grid.animals):
        plt.imshow(grid.grid_species[j], cmap='hot', interpolation='nearest')
        plt.savefig('visualization/heatmap/data_{}/map_animal_{}.png'.format(i,j))