import numpy as np
import matplotlib.pyplot as plt
import io
from sympy import latex, sin, symbols, cos
import matplotlib as ml
import random
import math
ml.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 14})

def f(x): #funct_1
    return np.sin(x)
def g(x): #funct_2
    return np.cos(x)
    
def to_canvas(a, b):
    x = 100*a+60
    y = 196-120*b
    #if b doesn't begin from 0, add (b-x) to shift b
    return [x,y]

def to_graph (a,b):
    x = (a-60)/100
    y = (b-196)/(-120)
    return [x,y]

def create_dict_xy_coord(p):
    return '{"x": ' + str(p[0]) + ',"y": ' + str(p[1]) + '}'

def generate(data):

    a = 0
    b = np.pi
    # randomly selects number of rectangles 
    n = random.choices([3,4,6])[0]
    
    # left or right Riemann summ 
    l_or_r = random.choices(["left","right"])[0]
    data["params"]["l_or_r"] = l_or_r
    
    # length of rectangle
    delta_x = (b-a)/n

    data["params"]["a"] = a
    data["params"]["b"] = b
    data["params"]["n"] = n
    data["params"]["delta_x"] = delta_x

    #generating where pi is on x-axis of pl-drawing-canvas
    pb = to_canvas (b, 0)
    data["params"]["pointb_x"] = str(pb[0])
    data["params"]["pointb_y"] = str(pb[1])
    
    #generating where pi/6 is on x-axis of pl-drawing canvas
    pb = to_canvas (b/6, 0)
    data["params"]["pointb2_x"] = str(pb[0])
    data["params"]["pointb2_y"] = str(pb[1])
    
    #generating where pi/3 is on x-axis of pl-drawing canvas
    pb = to_canvas (b/3, 0)
    data["params"]["pointb3_x"] = str(pb[0])
    data["params"]["pointb3_y"] = str(pb[1])
    #generating where pi/2 is on x-axis of pl-drawing canvas
    pb = to_canvas (b/2, 0)
    data["params"]["pointb4_x"] = str(pb[0])
    data["params"]["pointb4_y"] = str(pb[1])
    #generating where 2pi/3 is on x-axis of pl-drawing canvas
    pb = to_canvas (2*b/3, 0)
    data["params"]["pointb5_x"] = str(pb[0])
    data["params"]["pointb5_y"] = str(pb[1])
    #generating where 5pi/6 is on x-axis of pl-drawing canvas
    pb = to_canvas (5*b/6, 0)
    data["params"]["pointb6_x"] = str(pb[0])
    data["params"]["pointb6_y"] = str(pb[1])
    
    # this is the origin of the graph
    V0 = [60,196] # theoretically [60, 195] but 196 looks better for the pl-points

    #store origin points
    data["params"]["origin_x"] = str(V0[0])
    data["params"]["origin_y"] = str(V0[1])
    
    x = symbols('x')
    data["params"]["funct_1"] = latex(sin(x))
    data["params"]["funct_2"] = latex(cos(x))
    
    data["params"]["V_origin"] = create_dict_xy_coord([0,0])
    # numerical approximation calculation
    area = 0
    indices = np.linspace(0,np.pi,num = n)
    if (l_or_r == "left"):
        for ind in range(0,n):
            coor = (np.pi)*(1/n)*ind
            area += math.dist([f(coor)],[g(coor)])
    else:
        for ind in range(1,n+1):
            coor = (np.pi)*(1/n)*ind
            area += math.dist([f(coor)],[g(coor)])
    area *= (np.pi)*(1/n)     

    data["correct_answers"]["ans_sig"] = area
    
def parse(data):
    # makes sure accidental rectangles count as an invalid attempt
    n = data['params']['n']
    lines = data["submitted_answers"]["lines"]
    ans_rects = filter(lambda x : x['type'] == 'pl-rectangle', lines)
    if len(list(ans_rects)) != n:
        data['format_errors']['lines'] = 'Your answer must have the correct number of rectangles.'

def grade(data):
    # Custom grade of the plot to check whether n rectangles are placed correctly or not
    # correct pl-drawing-answer in html file is just a placeholder
    data_dict = data["submitted_answers"]["lines"]
    ans_sig_score = data["score"]
    usable_dict = []
    a = data['params']['a']
    b = data['params']['b']
    n = data['params']['n']
    delta_x = data['params']['delta_x']
    l_or_r = data['params']['l_or_r']
    # defining x and y tolerance using value of delta_x
    X_TOL = delta_x/5
    Y_TOL = delta_x/5
    
    # only stores pl-rectangles in usable_dict
    usable_dict = filter(lambda x : x['type'] == 'pl-rectangle', data_dict)

    graph_score = 0

    for d in usable_dict:
        # submitted width of rectangle converted to graph units
        submitted_width_gu = to_graph(d["width"],0)[0]-to_graph(0,0)[0]
        set_width = delta_x
        if (np.isclose(submitted_width_gu, set_width, atol = X_TOL)):
            if (l_or_r == "left"):
                # d.get("left") returns the center x-coordinate of rectangle
                gr_coor = to_graph(d["left"]-(1/2)*d["width"],0)[0]
            else:
                gr_coor = to_graph(d["left"]+(1/2)*d["width"],0)[0]
                
            hei_of_rec_calc = math.dist([f(gr_coor)],[g(gr_coor)])
            # d.get("height") returns individual height of rectangle; convert it to graph units
            hei_of_rec_submitted = to_graph (0,0)[1] -to_graph(0,d["height"])[1]
            if (np.isclose(hei_of_rec_calc,hei_of_rec_submitted, atol = Y_TOL)): 
                graph_score += (1/n)
            else:
                data["partial_scores"]["lines"]["feedback"] = "Make sure the heights of the rectangles are correct."
        else:
            data["partial_scores"]["lines"]["feedback"] = "Make sure the widths of the rectangles are correct."
    # correct graph is 75% of the correct answer, while the correct numerical approx is 25% of the correct answer
    data["score"] = graph_score*0.75+ans_sig_score*0.25
    


def file(data):
    # generates matplotlib graph
    if data['filename']=='figure1.png':
        # change a0 and b0 to change limit of the x-axis
        # 8 ticks on x-axis (400/8 = 50 pixels per tick)
        # 5 ticks on y-axis (300/5 = 60 pixels per tick)
        a0 = 0
        b0 = 4
        x = np.linspace(a0, b0, num=40)

        fig = plt.figure()
        ax = fig.add_subplot(111)

        major_ticks = np.arange(0, 4.1, 1)
        minor_ticks = np.arange(0, 4.1, 0.5)

        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        
        # Move bottom x-axis to centre, passing through (0,0)
        ax.spines['bottom'].set_position('center')
        
        # Eliminate upper and right axes
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        
        ax.xaxis.set_ticks_position('bottom')
        
        ax.grid(which='minor', alpha=0.2, linestyle='--')
        ax.grid(which='major', alpha=0.5)
        plt.plot(x,f(x),linewidth=3.0, label="f(x)")
        plt.plot(x,g(x),linewidth=3.0, label="g(x)")
        # adding legend denoting color of f(x) and g(x)
        ax.legend()
        plt.xlim(a0,b0)
        plt.ylim(-1.2,1.2)


    # Save the figure and return it as a buffer
    buf = io.BytesIO()
    plt.savefig(buf,format='png',transparent=True)
    return buf