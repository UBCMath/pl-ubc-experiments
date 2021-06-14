import random
import sympy

def generate(data):
    ambient = random.randint(15, 20)
    temp_ini = random.randint(24, 35)

    while (True):
        temp_fin = random.randint(21, 26)
        if(temp_fin< temp_ini):
            break

    time_ini = random.randint(1,6)
    
    m_or_night = ["am", "pm"]
    skip = ["Two", "Three", "Four", "Five"]

    time_of_day =  random.choices(m_or_night,k=1)[0]
    inc = "am" if (time_of_day == "pm") else "pm"
    
    hours_later =  random.choices(skip,k=1)[0]
    hours_pased = skip.index(hours_later) + 2 
    time_fin = time_ini + hours_pased
    K = sympy.Symbol('K', real = True)
    t = sympy.Symbol('t', real = True)
    k_const = sympy.solve ((temp_ini-ambient)*sympy.exp(K*hours_pased)+ambient-temp_fin,K)[0]
    t_d = sympy.solve(-37+ambient+(temp_ini-ambient)*sympy.exp(k_const*t),t)[0]
    mins = int(t_d*100)%100
    hours = int(t_d)
    list_of_para = {
        "ambient":  ambient, 
        "temp_ini" : temp_ini,
        "time_ini" : time_ini, 
        "time_fin" : time_fin,
        "temp_fin" : temp_fin, 
        "hours_later" : hours_later, 
        "time_of_day" : time_of_day,
        "incorrect_time_of_day" : inc,
        "const" : 45 }
    for key in list_of_para:
        data['params'][key] = list_of_para[key]
    
    data['correct_answers']['death_time_1'] = time_ini + hours
    data['correct_answers']['death_time_2'] = 45 + mins

