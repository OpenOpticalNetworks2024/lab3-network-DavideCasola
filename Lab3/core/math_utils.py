import numpy as np
import math


def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def lin2db(x):
    return 10*np.log10(x)


def db2lin(x):
    return 10**(x/10)