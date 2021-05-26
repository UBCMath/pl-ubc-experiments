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
        
        #adding labels to sides of figure
        ax.plot([-R, -R], [0, scale*R], "k")
        ax.plot([-R, -R], [0, scale*R], "ko")
        if (scale != 1):
            ax.text(-R-0.03, (scale*R)/2, str(scale) + "R", horizontalalignment="right", fontsize="xx-large", fontweight="black")
        else:
            ax.text(-R-0.03, (scale*R)/2, "R", horizontalalignment="right", fontsize="xx-large", fontweight="black")

        ax.plot([-R, 0], [scale*R,scale*R], "k")
        ax.plot([-R, 0], [scale*R,scale*R], "ko")
        ax.text((-R/2), scale*R, "R", verticalalignment="bottom", fontsize="xx-large", fontweight="black")

        ax.plot([0, R*np.cos(np.pi/4)], [scale*R,(R*np.sin(np.pi/4) + scale*R)], "k")
        ax.plot([0, R*np.cos(np.pi/4)], [scale*R,(R*np.sin(np.pi/4) + scale*R)], "ko")

        ax.text((R/2)-0.01, ((R/2)+scale*R)-0.01, "R", verticalalignment="top", fontsize="xx-large", fontweight="black")
        
        # adding new axes in the form of lines
        ax.plot([-2*R, 2*R], [0,0], "k")
        ax.plot([0, 0], [0, (scale*R+1.5*R)], "k")
        ax.text(2*R, 0, "x", verticalalignment="top", horizontalalignment="right", fontsize="x-large", fontweight="black")
        ax.text(0.1, (scale*R+1.5*R), "y", verticalalignment="top", horizontalalignment="right", fontsize="x-large", fontweight="black")
        

        plt.axis('off')
        plt.show()  

        # save plot as utf-8 bytes
        f = io.BytesIO()
        plt.savefig(f, format='png')
        return f

def generate(data):
    scale = random.randint(1,4)

    data['params']['scale'] = scale
    sympy.var('R')

    new_height = scale*R
    area_of_semicircle = (1/2)*np.pi*R**2
    area_of_rect = new_height*2*R
    com_semicircle = (4/(3*np.pi))*R + new_height
    com_rect = new_height/2
    y = area_of_semicircle*com_semicircle + area_of_rect* com_rect
    y = y/(area_of_rect+ area_of_semicircle)
    funct = sympy.lambdify (R, y)
    ans = funct (1)

    data['correct_answers']['y_coor'] = round (ans, 4)
    
    
