#!/usr/bin/python3

import math
import numpy as np

def wrap_to_pi(angle):
    """
    Limit an angle in radians to the range of [-pi, pi].
    param angle: the angle to be limited.
    :return: angle in radians limited  to the range of -pi to pi
    """
    wrapped_angle = np.mod(angle,  np.pi)
    times = np.floor_divide(angle, np.pi)
    wrapped_angle[np.mod(times, 2) == 1] = wrapped_angle[np.mod(times, 2) == 1] - np.pi
    return wrapped_angle


def euler_from_quaternion(x, y, z, w):
    """
    Convert a quaternion into euler angles (roll, pitch, yaw).

    param x: first component of quaternion form
    param y: second component of quaternion form
    param z: third component of quaternion form
    param w: fourth component of quaternion form
    :rtype: list[str]

    roll is rotation around x in radians (counterclockwise)
    pitch is rotation around y in radians (counterclockwise)
    yaw is rotation around z in radians (counterclockwise)
    
    Code from: https://automaticaddison.com/how-to-convert-a-quaternion-into-euler-angles-in-python/
    """
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll_x = math.atan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = math.asin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = math.atan2(t3, t4)
    return roll_x, pitch_y, yaw_z # in radians
