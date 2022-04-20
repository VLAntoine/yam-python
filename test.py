import numpy as np

SEED_ROOT = 10

np.random.seed(SEED_ROOT)

SEED_ARRAY = np.random.randint(0, high = 2**32-1, size = 48)


print(SEED_ARRAY)