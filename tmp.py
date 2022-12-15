import itertools
import random
import numpy as np
from cpmpy import *

'''
a = list(range(15))
b = list(range(15))
c = list(itertools.product(a, b))
test = np.zeros((5, 5))
tmp = test
d = list(itertools.permutations(c, 2))
list = [3,None,4,2]
print(list.shape)
'''
m = Model()
x = intvar(0, 100)
y = intvar(0, 100)
s = intvar(0, 100,shape=3)
m += (x <= (10 + s[0]))
m += (y <= (10 + s[1]))
m += (x + y >= 30 - s[2])
obj_fun = 1000*max(s) + sum(s)
m.minimize(obj_fun)
m.solve()
print(s.value())
