import random
import sympy

def generate(data):
    ambient = random.randint(15, 20)
    temp_ini = random.randint(26, 35)

    while (True):
        temp_fin = random.randint(21, 26)
        if(temp_fin< temp_ini):
            break

    time_ini = random.randint(1,6)
    skip = ["Two", "Three", "Four"]

    time_of_day = "pm"
    inc = "am"
    
    hours_later =  random.choices(skip,k=1)[0]
    hours_pased = skip.index(hours_later) + 2 
    time_fin = time_ini + hours_pased

    K = sympy.Symbol('K', real = True)
    t = sympy.Symbol('t', real = True)
    k_const = sympy.solve ((temp_ini-ambient)*sympy.exp(K*hours_pased)+ambient-temp_fin,K)[0]
    k_const = round(k_const, 5)
    t_d = float((1/k_const)*sympy.log((37-ambient)/(temp_ini-ambient)))
    mins = round(((abs(t_d*100)%100)/100)*60)
    if (t_d < 0):
        mins *= -1
    mins += 45
    hours = int(t_d)
    if ((hours + time_ini) <= 0 or (hours + time_ini) >= 12):
        time_of_day = "am"
        inc = "pm"
    while(mins >= 60):
        mins -= 60
        if (t_d > 0):
            hours += 1
        else:
            hours -= 1
    while(mins < 0):
        mins += 60
        if (t_d > 0):
            hours -= 1
        else:
            hours += 1        

    list_of_para = {
        "ambient":  ambient, 
        "temp_ini" : temp_ini,
        "time_ini" : time_ini, 
        "time_fin" : time_fin,
        "temp_fin" : temp_fin, 
        "hours_later" : hours_later, 
        "time_of_day" : time_of_day,
        "time_of_day_2" : inc,
        "const" : 45,
        "change_in_hr" : hours,
        "change_in_mins" : mins
    }
    for key in list_of_para:
        data['params'][key] = list_of_para[key]
    data['correct_answers']['death_time_h'] = time_ini + hours
    data ['correct_answers']['death_time_mins'] = mins

def grade(data):
    start_time_hr = data ['params']['time_ini'] 
    hours_sub = data ['submitted_answers']['death_time_h']
    mins_sub  = data ['submitted_answers']['death_time_mins']
    time = data ['submitted_answers']['time']
    change_in_hr = data ['params']['change_in_hr']
    if (data['score']!= 1):
        if ((hours_sub-change_in_hr) == (12+start_time_hr)):
            data['score'] += 1/3







