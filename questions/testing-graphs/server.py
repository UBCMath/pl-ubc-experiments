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

        left_endpoint = data['params']['left_endpoint'] 
        right_endpoint = data['params']['right_endpoint'] 
        
        xpoints = np.linspace(left_endpoint, right_endpoint, 1000)
        ypoints = xpoints
        fig.set_size_inches(5,5)

        plt.plot(xpoints, ypoints)
        # plt.axis('off')
        
        plt.tight_layout()
        plt.show()
        # save plot as utf-8 bytes
        f = io.BytesIO()
        plt.savefig(f, format='png', transparent=True,bbox_inches='tight', pad_inches=0)
        return f

def generate(data):
    

    left_endpoint = 0
    right_endpoint = 10
      
    data['params']['left_endpoint'] = left_endpoint
    data['params']['right_endpoint'] = right_endpoint



    

    

   
