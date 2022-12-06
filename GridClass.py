import numpy as np

import math
import pandas as pd
from matplotlib import pyplot as plt


class Grid:

    def __init__(self, width=10, height=10, initial_cost=1, animals=15,path=''):
        if path=='':
            self.width = width
            self.height = height
            self.animals = animals
            self.grid_cost = [[initial_cost for _ in range(self.width)]
                              for _ in range(self.height)]
            self.grid_cost = np.asarray(self.grid_cost)
            self.grid_species = [[[0 for _ in range(self.width)] for _ in range(self.height)] for _ in range(self.animals)]
            self.grid_species = np.asarray(self.grid_species)
        else:
            df = pd.read_csv(path)
            self.height = df['row'].max() + 1
            self.width = df['col'].max() + 1
            self.animals = len(df.columns) - 4
            self.grid_cost = [[initial_cost for _ in range(self.width)]
                              for _ in range(self.height)]
            self.grid_cost = np.asarray(self.grid_cost)
            self.grid_species = [[[0 for _ in range(self.width)] for _ in range(self.height)] for _ in
                                 range(self.animals)]
            self.grid_species = np.asarray(self.grid_species)

            for index, row in df.iterrows():
                index_row = row['row']
                index_col = row['col']
                self.grid_cost[index_row][index_col] = row['cost']
                for i in range(animals):
                    self.grid_species[i][index_row][index_col] = row['specie {}'.format(i)]




    def adds_specie(self, position, cov, size, index_specie):
        distribution = np.random.multivariate_normal(mean=position, cov=[[cov, 0], [0, cov]], size=size)
        for el in distribution:
            if el[0] < self.height and el[1] < self.width:
                self.grid_species[index_specie][math.floor(el[1])][math.floor(el[0])] += 1

    def add_rectangle_constant_cost(self, corner, width, height, cost):
        index_col = min(self.width, corner[1] + width)
        index_row = min(self.height, corner[0] + height)
        for row in range(corner[0], index_row):
            for col in range(corner[1], index_col):
                if self.grid_cost[row][col] < cost:
                    self.grid_cost[row][col] = cost

    def add_circle_constant_cost(self, center, radius, cost):
        index_1_row = max([0, center[0] - radius])
        index_2_row = min([self.height, center[0] + radius + 1])
        index_1_col = max([0, center[1] - radius])
        index_2_col = min([self.width, center[1] + radius + 1])
        for row in range(index_1_row, index_2_row):
            for col in range(index_1_col, index_2_col):
                if np.linalg.norm(np.asarray([row, col]) - np.asarray(center)) <= radius and \
                        self.grid_cost[row][col] < cost:
                    self.grid_cost[row][col] = cost

    def add_circle_gaussian_cost(self, center, radius, cost, std):
        index_1_row = max([0, center[0] - radius])
        index_2_row = min([self.height, center[0] + radius + 1])
        index_1_col = max([0, center[1] - radius])
        index_2_col = min([self.width, center[1] + radius + 1])
        for row in range(index_1_row, index_2_row):
            for col in range(index_1_col, index_2_col):
                multi = np.exp(-((row - center[0]) ** 2 + (col - center[1]) ** 2) / std ** 2)
                cost_cell = multi * cost
                if np.linalg.norm(np.asarray([row, col]) - np.asarray(center)) <= radius and \
                        self.grid_cost[row][col] < cost_cell:
                    self.grid_cost[row][col] = cost_cell

    def convert_into_df(self):
        list_dataframe = []
        list_number_specie = []
        for row in range(self.height):
            for col in range(self.width):
                info = []
                info.append(row)
                info.append(col)
                info.append(self.grid_cost[row, col])
                for animal in range(self.animals):
                    info.append(self.grid_species[animal][row][col])
                list_dataframe.append(info)
        for i in range(self.animals):
            list_number_specie.append('specie {}'.format(i))
        columns_df = ['row','col','cost']+list_number_specie
        df = pd.DataFrame(list_dataframe,columns=columns_df)
        return df

    def show_cost_map(self):
        plt.imshow(self.grid_cost, cmap='hot', interpolation='nearest')
        plt.show()

    def show_specie_map(self,index):
        plt.imshow(self.grid_species[index], cmap='hot', interpolation='nearest')
        plt.show()



