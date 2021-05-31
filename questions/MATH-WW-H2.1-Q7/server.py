import random

def generate(data):

    # Generate a random number that determines the middle x-intercept of the function
    n = random.randint(1, 8)
    l = 0   # left x-intercept
    r = 9   # right x-intercept

    data['params']['n'] = n
    data['params']['l'] = l
    data['params']['r'] = r