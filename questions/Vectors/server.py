import matplotlib.pyplot as plt
import matplotlib.patches as pcs
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
    data["params"]["r"] = float(r[1])
    data["params"]["s"] = float(s[0])
    data["params"]["rscale"] = rscale
    data["params"]["sscale"] = sscale

    # first scale our vectors, then sum them and rotate them with the rotational matrix
    # note that this is fine because
    # rot_matrix * rscale * r + rot_matrix * sscale * s = rot_matrix * (rscale * r + sscale * s)
    result = rot_matrix.dot(rscale * r + sscale * s)

    # add the correct answers for the x and y components to data["correct-answers"]
    data["correct_answers"]["x-comp"] = float(result[0])
    data["correct_answers"]["y-comp"] = float(result[1])

def file(data):
    if data["filename"] == "figure.png":

        theta = data["params"]["theta"]
        r = np.array([0, data["params"]["r"]])
        s = np.array([data["params"]["s"], 0])
        rot_matrix = np.array([[np.cos(theta * np.pi / 180), np.sin(theta * np.pi / 180)],
                            [-np.sin(theta * np.pi / 180), np.cos(theta * np.pi / 180)]])

        r = rot_matrix.dot(r)
        s = rot_matrix.dot(s)

        fig, ax = plt.subplots()
        ax.spines[["left", "bottom"]].set_position(("data", 0))
        ax.spines[["top", "right"]].set_visible(False)
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

        ax.set_xlim([0, 5])
        ax.set_ylim([-5, 5])
        ax.set_aspect("equal")

        ax.set_xticks([])
        ax.set_yticks([])

        ax.add_patch(pcs.Arc((0, 0), np.linalg.norm(r), np.linalg.norm(r), theta1=90-theta, theta2=90))
        ax.add_patch(pcs.Arc((0, 0), np.linalg.norm(s), np.linalg.norm(s), theta1=360-theta, theta2=0))

        ax.arrow(0, 0, r[0], r[1], color="#81b85d", lw=2)
        ax.arrow(0, 0, s[0], s[1], color="#81b85d", lw=2)

        ax.text(1.1*r[0]+0.3, 1.1*r[1], r"$\vec{r}$")
        ax.text(1.1*s[0]+0.3, 1.1*s[1], r"$\vec{s}$")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    return buf
