import random, math
import numpy as np
import prairielearn as pl
import scipy.linalg as sla
import to_precision

def generate(data):

    N = 3
    sf = 2
    a = np.array([1,2,3])
    b = np.array([2,4,6])
    B = np.array([0,0,0])
    C = np.array([0,0,0])
    #C = B / np.sqrt(np.dot(B, B))

    data["params"]["sf"] = sf
    data["params"]["a"] = pl.to_json(a)
    data["params"]["b"] = pl.to_json(b)

    data["correct_answers"]["out1"] = pl.to_json(B)
    data["correct_answers"]["out2"] = pl.to_json(C)
    