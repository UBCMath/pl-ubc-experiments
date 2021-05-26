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
        
        
        #remove ticks on axes
        plt.tick_params(
            axis='both',          
            which='both',      
            bottom=False,
            top=False,
            labelbottom=False,
            right=False,
            left=False,
            labelleft=False)
        
        #remove border on graph
        fig.patch.set_visible(False)
        ax.axis('off')
        
        # add initial base
        x = [-R, -R, R,R]
        y = [0, scale*R, scale*R, 0]
        plt.plot(x,y)
        
        theta = np.linspace(0, (np.pi/2), 100)
        
        x1 = R*np.cos(theta)
        x2 = R*np.sin(theta) + scale*R

        
        ax.plot(x1, x2)
        
        plt.show()  

        # save plot as utf-8 bytes
        f = io.BytesIO()
        plt.savefig(f, format='png')
        return f

def generate(data):
    scale = random.randint(1,4)

    data['params']['scale'] = scale
    sympy.var ('x y scale R')
    
    x = 0*R
    y = R

    data['correct_answers']['x_coor'] = pl.to_json(x)
    data['correct_answers']['y_coor'] = pl.to_json(y)
    
    
