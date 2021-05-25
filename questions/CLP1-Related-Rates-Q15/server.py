import random
import numpy as np
import matplotlib.pyplot as plt
import io

def generate(data):
    r = random.randint(3, 5)
    R = random.randint(r+1, 10)

    Dr = random.randint(1, 10)
    DR = random.randint(1, 10)

    data["params"]["r"] = r
    data["params"]["R"] = R
    data["params"]["Dr"] = Dr
    data["params"]["DR"] = DR

    # note that A(t) = π(R(t)^2 - r(t)^2), so by the chain rule, we have
    # dA/dt = π(2R dR/dt - 2r dr/dt) = 2π(R dR/dt - r dr/dt)
    rate_of_change = 2 * np.pi * (R * DR - r * Dr)

    data["correct_answers"]["rate_of_change"] = rate_of_change

def file(data):
    if data["filename"] == "figure.png":
        n, radii = 50, [data["params"]["r"], data["params"]["R"]]
        theta = np.linspace(0, 2*np.pi, n, endpoint=True)
        xs = np.outer(radii, np.cos(theta))
        ys = np.outer(radii, np.sin(theta))

        # in order to have a closed area, the circles
        # should be traversed in opposite directions
        xs[1,:] = xs[1,::-1]
        ys[1,:] = ys[1,::-1]

        # add the filled grey area of the annulus (the lines are a bit wonky so new borders have to be made)
        ax = plt.subplot(111, aspect='equal')
        ax.fill(np.ravel(xs), np.ravel(ys), "lightgrey", edgecolor='lightgrey')

        # add some edges to the annulus
        inner_rad = plt.Circle((0, 0), data["params"]["r"], fill=False,edgecolor="k")
        outer_rad = plt.Circle((0, 0), data["params"]["R"], fill=False,edgecolor="k")
        ax.add_patch(inner_rad)
        ax.add_patch(outer_rad)

        # plot lines for r and R, as well as a central dot
        ax.plot([0, data["params"]["R"]], [0, 0], "k")
        ax.plot([0, 0], [0, -data["params"]["r"]], "k")
        ax.plot(0, 0, "ko")

        # add labels for r and R
        ax.text(data["params"]["R"] / 2, 0.5, "R", horizontalalignment="center", fontsize="xx-large", fontweight="black")
        ax.text(-1, -data["params"]["r"] / 2, "r", verticalalignment="center", fontsize="xx-large", fontweight="black")

        # remove axes
        plt.axis("off")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    return buf
