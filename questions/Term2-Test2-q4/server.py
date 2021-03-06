import matplotlib.pyplot as plt
import matplotlib.patches as patches
import prairielearn as pl
import io
import random
from sympy import Symbol, pi, sqrt, integrate, simplify
import numpy as np
    
def file(data):
    if data['filename']=='figure.png':
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='auto', autoscale_on = True)
        #dummy value for R for graphing purposes
        R = 0.5
        scale = data['params']['scale']
        new_height = scale*R

        # plot rectangle base
        x = [-R, -R, R,R]
        y = [0, new_height, new_height, 0]
        plt.plot(x,y)
        
        # plot semicircle 
        theta = np.linspace(0, np.pi, 100)
        
        x1 = R*np.cos(theta)
        x2 = R*np.sin(theta) + new_height # vertical shift upwards

        ax.plot(x1, x2)
        ax.set_aspect(1)
        
        #adding labels to sides of figure
        ax.plot([-R, -R], [0, new_height], "k")
        ax.plot([-R, -R], [0, new_height], "ko")
        if (scale != 1):
            ax.text(-R-0.03, (new_height)/2, str(scale) + "R", horizontalalignment="right", fontsize="xx-large", fontweight="black")
        else:
            ax.text(-R-0.03, (new_height)/2, "R", horizontalalignment="right", fontsize="xx-large", fontweight="black")

        ax.plot([-R, 0], [new_height,new_height], "k")
        ax.plot([-R, 0], [new_height,new_height], "ko")
        ax.text((-R/2), new_height, "R", verticalalignment="bottom", fontsize="xx-large", fontweight="black")

        ax.plot([0, R*np.cos(np.pi/4)], [new_height,(R*np.sin(np.pi/4) + new_height)], "k")
        ax.plot([0, R*np.cos(np.pi/4)], [new_height,(R*np.sin(np.pi/4) + new_height)], "ko")

        ax.text((R/2)-0.01, ((R/2)+new_height)-0.01, "R", verticalalignment="top", fontsize="xx-large", fontweight="black")
        
        # adding new axes in the form of lines
        ax.plot([-2*R, 2*R], [0,0], "k")
        ax.plot([0, 0], [0, (new_height+1.5*R)], "k")
        ax.text(2*R, 0, "x", verticalalignment="top", horizontalalignment="right", fontsize="x-large", fontweight="black")
        ax.text(0.12, (new_height+1.5*R), "y", verticalalignment="top", horizontalalignment="right", fontsize="x-large", fontweight="black")
        
        # remopve original axes
        plt.axis('off')
        plt.show()  

        # save plot as utf-8 bytes
        f = io.BytesIO()
        plt.savefig(f, format='png')
        return f

def generate (data):
    scale = random.randint(1,4)

    data['params']['scale'] = scale
    x = Symbol('x', real=True)
    R = Symbol('R', real=True)
    
    m = pi*R**2/2 + 2*scale*R**2
    dybar = 1/(2*m)*(scale*R + sqrt(R**2 - x**2))**2
    y = simplify(integrate(dybar, (x, -R, R)))
    
    data['correct_answers']['y_coor'] = pl.to_json(y)
    
    
