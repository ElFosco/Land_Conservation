import itertools

import numpy as np

a = list(range(15))
b = list(range(15))
c = list(itertools.product(a, b))
test = np.zeros((5, 5))
tmp = test
d = list(itertools.permutations(c, 2))
print(d)
