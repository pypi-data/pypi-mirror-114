#Formula Page

import math


#factorial
def factorial(x):
    if x < 0:
        print("Invalid Input Value!")
    elif x == 1 or x == 0:
        return x
    else:
        i = 1
        for a in range(1, x+1):
            i *= a
            a+=1
        return i
#fibonacci
def fibonacci(x):
    if x<0:
        print("Incorrect Value")
    elif x == 0:
        return 0
    elif x == 1 or x == 2:
        return 1
    else:
        return fibonacci(x-1)+fibonacci(x-2)

#sum of all positive integers 

def sum_of_pos_int(x):
    if x > 0:
        a = 0
        for i in range(0,x+1):
            a += i
        return a
    else:
        print("Incorrect value")

#sum of positivr integers with power of x
#by range of ri to re
def sum_of_pos_int_pow(x,ri,re):
    power = 0
    base_num = x
    rangea = ri
    rangeb = re
    a = 0 
    for i in range(rangea,rangeb+1):
        power = i
        a += (base_num**power)
    return a

#Scientifics

#Mechanics

#Motion with constant velocity

#Instantaneous velocity

def mechanics_instant_velocity(x,t):
    v = x/t
    return round(v,4)

# Average Velocity

def mechanics_average_velocity(pos_init,pos_final,time_init,time_final):
    v = (pos_final - pos_init) / (time_final - time_init)
    return round(v,4)

#Motion with constant acceleration

#Displacement x

def mechanics_displacement_f1(vel_init,acce,time):
    x = (vel_init*time) + (0.5*(a*(time**2)))
    return round(x,4)

def mechanics_displacement_f2(vel_init,vel_final,time):
    x = ((vel_final+vel_init)/2)*time
    return round(x,4)

# final velocity vf

def mechanics_velocity_f_f1(vel_init,acce,time):
    vf = vel_init+(acce*time)
    return round(vf,4)
    
def mechanics_velocity_f_f2(vel_init,acce,pos):
    a = (vel_init**2) + (2*acce*pos)
    vf = math.sqrt(a)
    return round(vf,4)


# acceleration acce

def mechanics_acce_f1(vel_init,vel_final,time):
    acce = (vel_final - vel_init) / time
    return round(acce,4)
    
def mechanics_instant_acce(vel,time):
    acce = vel / time
    return round(acce,4)
    
def mechanics_average_acce(vel_final,vel_init,time_final,time_init):
    acce = (vel_final - vel_init) / (time_final - time_init)

