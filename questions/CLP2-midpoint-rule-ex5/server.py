import numpy as np
import matplotlib.pyplot as plt
import io
from sympy import latex, sin, symbols, pi
import matplotlib as ml
ml.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 14})

PI_CONST = round(float(pi),5)

def f(x):
    return np.sin(x)
    
def to_canvas(a, b):
    x = 100*a+60
    y = 345-250*b
    #if b doesn't begin from 0, add (b-x) to shift b
    return [x,y]

def to_graph (a,b):
    x = (a-60)/100
    y = (b-345)/(-250)
    return [x,y]

def create_dict_xy_coord(p):
    return '{"x": ' + str(p[0]) + ',"y": ' + str(p[1]) + '}'
    
def generate(data):

    a = 0
    b = PI_CONST
    n = 4
    
    # length of rectangle
    delta_x = (b-a)/n

    data["params"]["a"] = a
    data["params"]["b"] = b
    data["params"]["n"] = n
    data["params"]["delta_x"] = delta_x

    #generating where pi is on pl-drawing-canvas
    ftb = round(f(b),3)
    pb = to_canvas (b, ftb)
    data["params"]["pointb_x"] = str(pb[0])
    data["params"]["pointb_y"] = str(pb[1])
    
    # this is the origin of the graph
    V0 = [60,345]
    

    #store origin points
    data["params"]["origin_x"] = str(V0[0])
    data["params"]["origin_y"] = str(V0[1])
    
    x = symbols('x')
    data["params"]["funct"] = latex(sin(x))
    data["params"]["pi_rep"] = str(latex(pi))
    
    data["params"]["V_origin"] = create_dict_xy_coord([0,0])
    # numerical approximation for n = 4
    data["correct_answers"]["ans_sig"] = float(delta_x*(np.sin(PI_CONST/8)+np.sin(3*PI_CONST/8)+np.sin(5*PI_CONST/8)+np.sin(7*PI_CONST/8)))



def grade(data):
    # Custom grade of the plot to check whether n rectangles are placed correctly or not
    # correct pl-drawing-answer in html file is just a placeholder
    data_dict = data["submitted_answers"].get("lines")
    ans_sig_score = data["score"]
    usable_dict = []
    a = data['params']['a']
    b = data['params']['b']
    n = data['params']['n']
    delta_x = data['params']['delta_x']
    set_width = to_canvas(delta_x,0)[0]-60
    
    for d in data_dict:
        # only stores pl-rectangles in usable_dict
        if(d.get("type") == "pl-rectangle"):
            usable_dict.append(d)
    graph_score = 0
    if (len (usable_dict) != n):
        data["partial_scores"]["lines"]["feedback"] = "Make sure you have placed the correct number of rectangles."
    else:
        for d in usable_dict:
            if (np.isclose(d.get("width"), set_width, atol = 10.0)):
                # d.get("left") returns the center x-coordinate of rectangle
                left_ind = to_graph((d.get("left")),0)[0]
                f_of_midpoint_ind = to_canvas (0,f(left_ind))[1]
                # d.get("height") returns individual height of rectangle; 345- this value to get position of f(midpoint) 
                if (np.isclose(345-d.get("height"),f_of_midpoint_ind, atol = 20.0)):
                    graph_score += (1/n)
            else:
                data["partial_scores"]["lines"]["feedback"] = "Make sure the widths of the rectangles are correct."
    # correct graph is 75% of the correct answer, while the correct numerical approx is 25% of the correct answer
    data["score"] = graph_score*0.75+ans_sig_score*0.25
    
    


def file(data):
    # generates matplotlib graph
    if data['filename']=='figure1.png':
        # change a0 and b0 to change limit of axes
        # current configuration is 50 pixels for each tick
        # 8 ticks on x-axis and 6 ticks on y-axis
        a0 = 0
        b0 = 4
        x = np.linspace(a0, b0, num=40)

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