import random
import math
import numpy as np
import matplotlib.pyplot as plt
import io
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
    return [x,y]
    
    
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


def parse(data):
    # makes sure exactly one line and one point is placed by the user 
    lines = data["submitted_answers"]["lines"]
    # this means no additional elements were placed by user 
    if lines is None:
        data['format_errors']['lines'] = "Graph submission is NOT valid. Please add one line and one point to the graph area."
    else:
        ans_lines = filter(lambda x : x["type"] == 'pl-controlled-line', lines)
        ans_dots = filter(lambda x : (x['graded'] == 1) and x["type"] == 'pl-point', lines)
        if len(list(ans_lines)) != 1 or len(list(ans_dots)) != 1:
            data['format_errors']['lines'] = "Graph submission is NOT valid. Exactly one line and one point should be added to the graph area"

        
def grade(data):
    # Custom grade of the plot. Checking the slope of the plot
    graph = data["submitted_answers"]["lines"]
    
    # defining error tolerance of grading line/point
    SLOPE_TOL = 0.5
    # checking whether derivative at this x-coordinate matches the slope of secant or not
    X_TOL = 3

    # only storing items placed by student
    # convert to list first; if not will raise 'filter' object is not subscriptable error
    item_line = list(filter(lambda x : x["type"] == 'pl-controlled-line', graph))[0]
    item_point = list(filter(lambda x : (x['graded'] == 1) and x["type"] == 'pl-point', graph))[0]
    
    x_coor = to_graph(item_point['left'],0)[0]

    #checking if x coordinate of placed point satisfies MVT
    #print(x_coor,df(x_coor,data["params"]["a"], data["params"]["b"]),data["params"]["slope_of_secant"])
    if np.allclose(df(x_coor,data["params"]["a"], data["params"]["b"]), data["params"]["slope_of_secant"], atol=X_TOL):
        data["partial_scores"]["lines"]["score"] += 0.5
        
    st_slope = (item_line['y2'] - item_line['y1'])/ (item_line['x2'] - item_line['x1'] )
    if np.allclose(st_slope, data["params"]["slope_canvas"], rtol=SLOPE_TOL):
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