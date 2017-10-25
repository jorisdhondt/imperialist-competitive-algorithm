import numpy as np
import random as rn

def generator(resources,tasks):
    candidate = np.random.choice(resources,tasks)
    return np.array(candidate)


def randomSelection(P):
    r = rn.random()

    C = np.cumsum(P)

    index = [i for i, x in enumerate(C) if r <= x]

    return index[0]  # we only need the first entry that statisfies the check