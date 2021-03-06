import random

def generate(data):

    # Generate a random number that determines the y-intercept of the function
    n = random.randint(1, 9)

    data['params']['n'] = n

    data['correct_answers']['lim-L'] = str(-n)
    data['correct_answers']['lim-R'] = str(n)
    data['correct_answers']['lim'] = "DNE"