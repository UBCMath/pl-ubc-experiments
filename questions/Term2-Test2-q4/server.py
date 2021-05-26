import matplotlib.pyplot as plt
import matplotlib.patches as patches
import prairielearn as pl
import io
import random
import sympy
import numpy as np
    
def file(data):
    if data['filename']=='figure.png':
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='auto', autoscale_on = True)
        R = 0.5
        scale = data['params']['scale']

        # add initial base
        x = [-R, -R, R,R]
        y = [0, scale*R, scale*R, 0]
        plt.plot(x,y)
        
        theta = np.linspace(0, np.pi, 100)
        
        x1 = R*np.cos(theta)
        x2 = R*np.sin(theta) + scale*R

        
        ax.plot(x1, x2)
        ax.set_aspect(1)
        
        #adding labels to sides
        ax.plot([-R, -R], [0, scale*R], "k")
        ax.plot([-R, -R], [0, scale*R], "ko")

        ax.text(-R-0.1, (scale*R)/2, scale, horizontalalignment="right", fontsize="xx-large", fontweight="black")
        ax.text(-R-0.01, (scale*R)/2, "R", horizontalalignment="right", fontsize="xx-large", fontweight="black")

        ax.plot([-R, 0], [scale*R,scale*R], "k")
        ax.plot([-R, 0], [scale*R,scale*R], "ko")
        ax.text((-R/2), scale*R, "R", verticalalignment="bottom", fontsize="xx-large", fontweight="black")

        ax.plot([0, R*np.cos(np.pi/4)], [scale*R,(R*np.sin(np.pi/4) + scale*R)], "k")
        ax.plot([0, R*np.cos(np.pi/4)], [scale*R,(R*np.sin(np.pi/4) + scale*R)], "ko")

        ax.text((R/2), ((R/2)+scale*R), "R", verticalalignment="top", fontsize="xx-large", fontweight="black")

        plt.axis('off')
        plt.show()  

        # save plot as utf-8 bytes
        f = io.BytesIO()
        plt.savefig(f, format='png')
        return f

def generate(data):
    scale = random.randint(1,4)

    data['params']['scale'] = scale
    x = sympy.symbols("x")
    sympy.var ('x y new_height R')
    new_height = scale*R
    
    area = new_height*(2*R)+(1/2)*(np.pi)*R**2
    semicircle_equation = new_height + np.sqrt(R**2-x**2)
    integrate_eq = (1/area)*sympy.integrate(semicircle_equation**2,R)
    Y = sympy.lambdify (R, integrate_eq)
    y = Y(R) -Y(0)

    data['correct_answers']['x_coor'] = pl.to_json(x)
    data['correct_answers']['y_coor'] = pl.to_json(y)
    
    
