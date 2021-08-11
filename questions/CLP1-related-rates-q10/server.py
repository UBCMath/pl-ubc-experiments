import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
from random import randint
from sympy import symbols
from numpy import diff

def file(data):
    if data['filename']=='figure.png':
        fig = plt.figure()
        ax = fig.add_subplot(111, aspect='auto', autoscale_on = True)
        
        #graph in metres 
        
        w = data['params']['w'] 
        b = data['params']['b'] /100
        h = data['params']['h'] /100
        l = data['params']['l']
        n = data['params']['now_height'] /100
        
        a = (w-b)*(1/2)

        #perspective for the right and top parallelograms
        shift = 0.45

        #top parallelogram 
        x = [0, w, (l+w-shift), (l-shift)]
        y = [h, h, (h+shift), (h+shift)]
        ax.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=False))
        
        #right parallelogram
        x = [w, (l+w-shift), (l+a+b-shift), (a+b)]
        y = [h, (h+shift), shift, 0]
        ax.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=False))
        
        #trapezoid 

        x = [0, w, (a+b),a]
        y = [h, h, 0, 0]
        ax.add_patch(patches.Polygon(xy=list(zip(x,y)), fill=False))
        
        # add dotted line showing current water level
        plt.plot([0,w],[n,n], linestyle = 'dotted')
        
        plt.axis('off')
        plt.show()  

        # save plot as utf-8 bytes
        f = io.BytesIO()
        plt.savefig(f, format='png')
        return f

def generate(data):
    l = randint(2,6)
    h = randint(30, 70)
    w = randint (1, 2)
    b = randint (20, 80)
    rate = randint (1, 3)
    
    while (True):
        now_height= randint(5, 50)
        if (now_height < h):
            break
      
    data['params']['l'] = l
    data['params']['h'] = h
    data['params']['w'] = w
    data['params']['b'] = b
    data['params']['rate'] = rate
    data['params']['now_height'] = now_height
    
    l = 100* l #change from m to cm
    w = 100* w

    x = symbols("x")
    v = b*l*x+(0.5)*(1/h)*l*x**2*(w-b)
    dv = v.diff(x)
    ans = float(dv.subs(x, now_height))
    
    rateToCmCubed = rate*-1000
    ans = (-1)*rateToCmCubed/ans
    data['correct_answers']['ans_sig'] = ans

    



    
