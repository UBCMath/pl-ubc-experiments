import numpy as np
import random
import pltikz

def generate(data):
    theta = random.randint(10, 80)
    Dtheta = round(random.uniform(0.0, 1.0), 2)
    data["params"]["theta"] = theta
    data["params"]["Dtheta"] = Dtheta
    # D = l * sin(θ), so we have
    # dD/dt = l * dθ/dt * cos(θ)
    data["correct_answers"]["DD"] = 2 * Dtheta * np.cos(theta * np.pi / 180)

def file(data):
    if data["filename"] == "figure.png":
        theta = data["params"]["theta"]
        theta_rads = theta * np.pi / 180
        figure = pltikz.TikZFigure("template.tex")
        return figure.image(params=data["params"],
                            sin_theta=np.sin(theta_rads),
                            cos_theta=np.cos(theta_rads),
                            sin_half_theta=np.sin(theta_rads/2),
                            cos_half_theta=np.cos(theta_rads/2))
