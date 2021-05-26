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

        
        # add dotted line showing current water level
        plt.plot([-R,0],[-R,scale*R], linestyle = 'dotted')
        
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
    
    
