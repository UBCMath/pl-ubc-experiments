from matplotlib import scale
import matplotlib.pyplot as plt
import numpy as np
import random
import io

def generate(data):

    # initialize the angle and the r and s vectors
    theta = random.randint(1, 89)
    r = np.array([0, random.randint(1, 5)])
    s = np.array([random.randint(1, 5), 0])
    rscale = random.randint(1, 5)
    sscale = random.randint(1, 5)

    # define the 2D (clockwise) rotation matrix, adjust by pi/180 for question being in terms of degrees
    rot_matrix = np.array([[np.cos(theta * np.pi / 180), np.sin(theta * np.pi / 180)],
                          [-np.sin(theta * np.pi / 180), np.cos(theta * np.pi / 180)]])

    # add them to data["params"]
    data["params"]["theta"] = theta
    data["params"]["r"] = r[1]
    data["params"]["s"] = s[0]
    data["params"]["rscale"] = rscale
    data["params"]["sscale"] = sscale

    # first scale our vectors, then sum them and rotate them with the rotational matrix
    # note that this is fine because
    # rot_matrix * rscale * r + rot_matrix * sscale * s = rot_matrix * (rscale * r + sscale * s)
    result = rot_matrix.dot(rscale * r + sscale * s)

    # add the correct answers for the x and y components to data["correct-answers"]
    data["correct-answers"]["x-comp"] = result[0]
    data["correct-answers"]["y-comp"] = result[1]

def file(data):
    if data["filename"] == "figure.png":

        # for plotting purposes it turns out to be easier to collect r and s in a matrix
        vectors = np.array([[data["params"]["s"], 0],
                            [0, data["params"]["r"]]])

        # redefine the 2D (clockwise) rotation matrix
        rot_matrix = np.array([[np.cos(data["params"]["theta"]), np.sin(data["params"]["theta"])],
                              [-np.sin(data["params"]["theta"]), np.cos(data["params"]["theta"])]])

        # apply our rotation to the vectors
        vectors = np.matmul(rot_matrix, vectors)

        # both r and s have their origin at (0, 0)
        origin = np.array([[0, 0], [0, 0]])

        plt.quiver(*origin, vectors[:,0], vectors[:,1], scale=1, units="xy")
        plt.grid()
        plt.xlim([0, 5])
        plt.ylim([-5, 5])

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    return buf
