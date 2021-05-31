import random
def generate (data):
    b = random.randint(100000,900000)

    data['params']['blank'] = b

    data['correct_answers']['c'] = 1
    data['correct_answers']['c2'] = b
    data['correct_answers']['c3'] = 0
    
    
