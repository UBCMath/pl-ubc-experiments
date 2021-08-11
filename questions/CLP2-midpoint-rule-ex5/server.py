import random
import math
import numpy as np
import matplotlib.pyplot as plt
import io
from sympy import latex, sin, symbols, pi
import matplotlib as ml
ml.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 14})

PI_CONST = round(float(pi),5)
def create_dict_xy_coord(p):
    return '{"x": ' + str(p[0]) + ',"y": ' + str(p[1]) + '}'

def f(x):
    return np.sin(x)
    
def to_canvas(a, b):
    x = 100*a+60
    y = 345-250*b
    return [x,y]
    #each tick is 50

def to_graph (a,b):
    x = (a-60)/100
    y = (b-345)/(-250)
    return [x,y]

def generate(data):

    # equation coefficients
    a = random.choice([0,PI_CONST/2])
    b = PI_CONST

    data["params"]["a"] = a
    data["params"]["b"] = b


    # corresponding function values
    fta = round(f(a),3)
    ftb = round(f(b),3)
    
    #generating point_a and point_b coordinates on pl-drawing-canvas
    pa = to_canvas (a, fta)
    pb = to_canvas (b, ftb)
    data["params"]["pointa_x"] = str(pa[0])
    data["params"]["pointa_y"] = str(pa[1])
    data["params"]["pointb_x"] = str(pb[0])
    data["params"]["pointb_y"] = str(pb[1])
    
    # this is the origin of the graph
    V0 = [60,345]
    

    #store origin points
    data["params"]["origin_x"] = str(V0[0])
    data["params"]["origin_y"] = str(V0[1])
    x = symbols('x')
    data["params"]["funct"] = latex(x)
    
    data["params"]["V_origin"] = create_dict_xy_coord([0,0])
    data["params"]["line"] = '[' + create_dict_xy_coord(pa) + ',' + create_dict_xy_coord(pb) + ']'



def grade(data):
    # Custom grade of the plot. Checking the slope of the plot
    data_dict = data["submitted_answers"].get("lines")
    usable_dict = []
    for d in data_dict:
        if(d.get("type") == "pl-rectangle"):
            usable_dict.append(d)
    
    print(usable_dict)


## The function 'file(data)' is used to generate the figure dynamically,
## given data defined in the 'generate' function
def file(data):

    if data['filename']=='figure1.png':
        a0 = 0
        b0 = 4
        x = np.linspace(a0, b0, num=40)
        a = data['params']['a']
        b = data['params']['b']

        fig = plt.figure()
        ax = fig.add_subplot(111)

        major_ticks = np.arange(0, 4.1, 1)
        minor_ticks = np.arange(0, 4.1, 0.5)
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        plt.plot(x,f(x),linewidth=3.0)
        plt.xlim(a0,b0)
        plt.ylim(0,1.2)
        plt.xlabel(r"$x$", fontsize=20)
        plt.ylabel(r"$f(x)$", fontsize=20)


    # Save the figure and return it as a buffer
    buf = io.BytesIO()
    plt.savefig(buf,format='png',transparent=True)
    return buf