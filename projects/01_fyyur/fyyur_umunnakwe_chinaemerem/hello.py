# import useful_functions as uf

# scores = [88, 92, 79, 93, 85]

# mean = uf.mean(scores)
# curved = uf.add_five(scores)

# mean_c = uf.mean(curved)

# print("Scores:", scores)
# print("Original Mean:", mean, " New Mean:", mean_c)

# print(__name__)
# print(uf.__name__)

# Why use NumPy?
import time
import numpy as np
x = np.random.random(100000000)

# Case 1
start = time.time()
sum(x) / len(x)
print(time.time() - start)

# Case 2
start = time.time()
np.mean(x)
print(time.time() - start)