import time
import math
import serial
import matplotlib.pyplot as plt

def detect():
    ser = serial.Serial('COM5', 9600) #komunikacja szeregowa z akcelerometrem
    values = [0, 0, 0]
    ax_list = []
    ay_list = []
    ax_actual = 0
    ay_actual = 0
    ax_previous = 0
    ay_previous = 0
    vx = 0
    vy = 0
    vx_list = [0]
    vy_list = [0]
    magnitude_v = [0]
    low_value = 0
    angles = -1
    s_time = time.time()
    for m in range(5):
        data = ser.readline()
        data = data.decode()
        data = data.strip()
        values = data.split(" ")
        values = [float(v) for v in values]
        ax_list.append((values[0]) * 0.2)
        ay_list.append((values[1]) * 0.2)
    ax_previous = sum(ax_list)
    ay_previous = sum(ay_list)
    for i in range(400):
        s_time = time.time()
        data = ser.readline()
        data = data.decode()
        data = data.strip()
        values = data.split(" ")
        values = [float(v) for v in values]
        #Średnia krocząca
        ax_list.append((values[0]) * 0.2)
        ay_list.append((values[1]) * 0.2)
        ax_actual = ax_list[i] + ax_list[i + 1] + ax_list[i + 2] + ax_list[i + 3] + ax_list[i + 4]
        ay_actual = ay_list[i] + ay_list[i + 1] + ay_list[i + 2] + ay_list[i + 3] + ay_list[i + 4]
        #Całkowanie metodą trapezów w celu otrzymania prędkości
        vx = (ax_actual + ax_previous) * 2 / (time.time() - s_time)
        vy = (ay_actual + ay_previous) * 2 / (time.time() - s_time)
        vx_list.append(vx + vx_list[i])
        vy_list.append(vy + vy_list[i])
        magnitude_v.append(math.sqrt(vx*vx + vy*vy))
        #Zliczanie ilości kątów narysowanej figury
        if (magnitude_v[i] < 30):
            low_value += 1
        else:
            low_value = 0
        if low_value == 15:
            angles += 1
    return angles
