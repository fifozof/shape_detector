import time
import math
import serial


def detect():
    ax = []
    ay = []
    tim = [0]
    act_acc_x = []
    act_acc_y = []
    ser = serial.Serial('COM6', 9600)
    values = [0, 0, 0]
    vx = 0
    vy = 0
    mag_v = [0]
    m_acc_x = 0
    m_acc_y = 0
    m_acc_last_x = 0
    m_acc_last_y = 0
    vx_vec = [0]
    vy_vec = [0]
    pretty_constant = 0
    angles = -1
    s_time = time.time()
    for m in range(5):
        data = ser.readline()
        data = data.decode()
        data = data.strip()
        values = data.split(" ")
        values = [float(v) for v in values]
        act_acc_x.append((values[0]) * 0.2)
        act_acc_y.append((values[1]) * 0.2)
    m_acc_last_x = sum(act_acc_x)
    m_acc_last_y = sum(act_acc_y)
    for i in range(400):
        s_time = time.time()
        data = ser.readline()
        data = data.decode()
        data = data.strip()
        values = data.split(" ")
        values = [float(v) for v in values]
        act_acc_x.append((values[0]) * 0.2)
        act_acc_y.append((values[1]) * 0.2)
        m_acc_x = act_acc_x[i] + act_acc_x[i + 1] + act_acc_x[i + 2] + act_acc_x[i + 3] + act_acc_x[i + 4]
        m_acc_y = act_acc_y[i] + act_acc_y[i + 1] + act_acc_y[i + 2] + act_acc_y[i + 3] + act_acc_y[i + 4]
        vx = (m_acc_x + m_acc_last_x) * 2 / (time.time() - s_time)
        vy = (m_acc_y + m_acc_last_y) * 2 / (time.time() - s_time)
        vx_vec.append(vx + vx_vec[i])
        vy_vec.append(vy + vy_vec[i])
        mag_v.append(math.sqrt(vx*vx + vy*vy))
        tim.append(tim[i] + time.time() - s_time)
        if i > 4:
            if (mag_v[i - 1] - 20 < mag_v[i] < mag_v[i - 1] + 20) and (mag_v[i - 2] - 20 < mag_v[i] < mag_v[i - 2] + 20) and (mag_v[i - 3] - 20 < mag_v[i] < mag_v[i - 3] + 20) and (mag_v[i - 4] - 20 < mag_v[i] < mag_v[i - 4] + 20):
                pretty_constant += 1
            else:
                pretty_constant = 0
            if pretty_constant == 20:
                angles += 1
    return angles
