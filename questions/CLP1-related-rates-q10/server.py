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
        
        w = data['params']['w'] 
        b = data['params']['b'] /100
        h = data['params']['h'] /100
        l = data['params']['l']
        n = data['params']['nowHeight'] /100
        
        a = (w-b)*(1/2)
        shift = 0.45
        
        
        #top parallelogram 
        x = [0, w, (l+w-shift), (l-shift)]
        y = [h, h, (h+shift), (h+shift)]
        ax.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=False))
        
        #right parallelogram
        x = [w, (l+w-shift), (l+a+b-shift), (a+b)]
        y = [h, (h+shift), shift, 0]
        ax.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=False))
        
        #trapezoid in cm

        x = [0, w, (a+b),a]
        y = [h, h, 0, 0]
        ax.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=False))
        plt.plot([0,w],[n,n], linestyle = 'dotted')
        
        plt.show()  

        # save plot as utf-8 bytes
        f = io.BytesIO()
        plt.savefig(f, format='png')
        return f

def generate(data):
    l = random.randint(2,6)
    lToCm = 100* l
    h = random.randint(30, 70)
    w = random.randint (1, 2)
    wToCm = 100* w
    b = random.randint (20, 80)
    rate = random.randint (1, 3)
    while (True):
        nowHeight= random.randint(5, 50)
        if (nowHeight < h):
            break
    x = sympy.symbols("x")
    v = b*lToCm*x+(0.5)*(1/h)*lToCm*x**2*(wToCm-b)
    dv = sympy.lambdify(x, v.diff(x))
    ans = dv(nowHeight)
    rateToCmCubed = rate*-1000
    ans = (-1)*rateToCmCubed/ans
    

    data['params']['l'] = l
    data['params']['h'] = h
    data['params']['w'] = w
    data['params']['b'] = b
    data['params']['rate'] = rate
    data['params']['nowHeight'] = nowHeight
    data['correct_answers']['ans_sig'] = round(ans,6)


    
