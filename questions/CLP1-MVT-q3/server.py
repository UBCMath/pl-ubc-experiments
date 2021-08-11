import random
import math
import numpy as np
import matplotlib.pyplot as plt
import io
import sympy
import matplotlib as ml
ml.rcParams['text.usetex'] = True
plt.rcParams.update({'font.size': 14})

def create_dict_xy_coord(p):
    return '{"x": ' + str(p[0]) + ',"y": ' + str(p[1]) + '}'

def f(x,a,b,c):
    return -a*x**4 + b*x**2 + c

def df(x,a,b):
    return -4*a*x**3 + 2*b*x
    
def to_canvas(a, b):
    x = 200*a+60
    y = 345-10*(b-10)
    #if b doesn't begin from 0, add (b-x) to shift b
    return [x,y]

def to_graph (a,b):
    x = (a-60)/200
    y = (b-445)/(-10)
    return [int(x),y]
    
    
def generate(data):

    # equation coefficients
    a = random.randint(9,12)
    b = random.randint(10,13)
    c = random.randint(28,35)
    #choosing where point b is so that it exists on the png
    while(True):
        choice_of_b = random.choice ([1.20, 1.30, 1.40])
        if(round(f(choice_of_b,a,b,c),1) >= 10):
            break
        
    data["params"]["a"] = a
    data["params"]["b"] = b
    data["params"]["c"] = c

    # corresponding function values
    fta = round(f(0,a,b,c),1)
    ftb = round(f(choice_of_b,a,b,c),1)
    
    #generating point_a and point_b coordinates on pl-drawing-canvas
    pa = to_canvas (0, fta)
    pb = to_canvas (choice_of_b, ftb)
    data["params"]["pointa_x"] = str(pa[0])
    data["params"]["pointa_y"] = str(pa[1])
    data["params"]["pointb_x"] = str(pb[0])
    data["params"]["pointb_y"] = str(pb[1])
    
    # this is the origin of the graph
    V0 = [60,345]
    
    # find slope of secant
    slope_of_secant = (ftb-fta) / choice_of_b
    data["params"]["slope_of_secant"] = slope_of_secant
    
    data["params"]["slope_canvas"] = (pb[1] - pa[1])/(pb[0] - pa[0])

    #store origin points
    data["params"]["origin_x"] = str(V0[0])
    data["params"]["origin_y"] = str(V0[1])
    
    data["params"]["V_origin"] = create_dict_xy_coord([0,0])
    data["params"]["line"] = '[' + create_dict_xy_coord(pa) + ',' + create_dict_xy_coord(pb) + ']'



def grade(data):
    # Custom grade of the plot. Checking the slope of the plot
    graph = data["submitted_answers"].get("lines")
    # the above line will not fail, since the element parse function will fail if no submission is added to the plot area
    gradable_dict = []
    
    # only adding items placed by student into gradable_dict
    for g in graph:
        if(g.get("placed_by_user") == 1):
            gradable_dict.append(g)
    
    if (len(gradable_dict) != 2):
        data["partial_scores"]["lines"]["feedback"] = "Graph submission is NOT valid! Exactly one line and one point should be added to the graph area"
        data["partial_scores"]["lines"]["score"] = 0
    else:
        if (gradable_dict[0].get("type") == "pl-point"):
            item_point = gradable_dict[0]
            item = gradable_dict[1]
        else :
            item = gradable_dict[0]
            item_point = gradable_dict[1]

        canvas_to_graph = (item_point['left'] -60 )/200
        
        #checking if x coordinate of placed point satisfies MVT
        if np.allclose(df(canvas_to_graph,data["params"]["a"] ,data["params"]["b"]),  data["params"]["slope_of_secant"] , atol=3):
            data["partial_scores"]["lines"]["score"] += 0.5
        st_slope = (item['y2'] - item['y1'])/ (item['x2'] - item['x1'] )
        if np.allclose(st_slope, data["params"]["slope_canvas"], rtol=0.5):
            data["partial_scores"]["lines"]["score"] += 0.5
            data["partial_scores"]["lines"]["feedback"] = "The secant line is correct"
        else:
            data["partial_scores"]["lines"]["feedback"] = "The secant line is NOT correct"

    # recomputing final score based on partial scores
    total_score = 0
    for var in data["partial_scores"]:
        partial_score = data["partial_scores"][var]["score"]
        total_score += partial_score
    data["score"] = total_score/len(data["partial_scores"])

## The function 'file(data)' is used to generate the figure dynamically,
## given data defined in the 'generate' function
def file(data):

    if data['filename']=='figure1.png':
        a0 = 0
        b0 = 2
        x = np.linspace(a0, b0)
        a = data['params']['a']
        b = data['params']['b']
        c = data['params']['c']

        fig = plt.figure()
        ax = fig.add_subplot(111)

        major_ticks = np.arange(0, 2.1, 0.25)
        minor_ticks = np.arange(0, 2.1, 0.125)
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        plt.plot(x,f(x,a,b,c),linewidth=3.0)
        plt.xlim(a0,b0)
        plt.ylim(10,40)
        plt.xlabel(r"$x$", fontsize=20)
        plt.ylabel(r"$f(x)$", fontsize=20)


    # Save the figure and return it as a buffer
    buf = io.BytesIO()
    plt.savefig(buf,format='png',transparent=True)
    return buf