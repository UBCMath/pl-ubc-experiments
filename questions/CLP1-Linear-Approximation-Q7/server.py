from sympy import var
import random

def generate(data):

    # Generate params
    a = random.randint(3, 5)
    b = random.randint(1, 4)
    b = 10+(1/10)*b
    
    var ('a b')
    data['params']['a'] = a
    data['params']['b'] = b

    data['correct_answers']['cons_ans'] = 10**a
    data['correct_answers']['linear_ans'] = round(10**a+a*(10)**(a-1)*(b-10))
