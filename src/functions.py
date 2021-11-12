from math import sin, cos, radians as rd, sqrt

import globals as gb


def get_array_x(x_start, speed, alpha, time):
    array = [[], []]

    t = 0.0
    while True:
        x = x_start + (round(cos(rd(alpha)), 5) * speed * t)
        t += 0.001

        if t > time:
            return array

        array[0].append(t)
        array[1].append(x)


def get_array_y(y_start, speed, alpha, time):
    array = [[], []]

    t = 0.0
    while True:
        y = y_start + (sin(rd(alpha)) * speed * t) - ((gb.g * t ** 2) / 2)
        t += 0.001

        if t > time:
            return array

        array[0].append(t)
        array[1].append(y)


def get_array_s(x_start, y_start, speed, alpha, time):
    array_x = get_array_x(x_start, speed, alpha, time)
    array_y = get_array_y(y_start, speed, alpha, time)

    array_s = [[], []]
    s, last_x, last_y = 0, 0, 0

    for i in range(len(array_x[0])):
        s += sqrt(abs(last_x - array_x[1][i]) ** 2 +
                  abs(last_y - array_y[1][i]) ** 2)

        last_x = array_x[1][i]
        last_y = array_y[1][i]

        array_s[0].append(array_x[0][i])
        array_s[1].append(s)

    return array_s


def get_flight_time(y_start, speed, alpha):
    return (speed * sin(rd(alpha)) +
            sqrt((speed * sin(rd(alpha))) ** 2 + 2 * gb.g * y_start)) / gb.g
