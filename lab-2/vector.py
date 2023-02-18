import math


# 2D vector normalization
def v_norm_2d(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


# 2D vectors addition
def v_add_2d(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]


# 2D vectors subtraction
def v_sub_2d(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]


# 2D vector multiply with a scalar
def v_mult_2d(v, scalar):
    return [v[0] * scalar, v[1] * scalar]


# 2D vector division by a scalar
def v_div_2d(v, scalar):
    if scalar == 0:
        return v
    return [v[0] / scalar, v[1] / scalar]


# 2D vectors dot product
def v_dot_2d(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


# Angle to vector
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


# Distance between 2D vectors
def v_dist_2d(v1, v2):
    return math.sqrt((v1[0] - v2[0]) ** 2 + (v1[1] - v2[1]) ** 2)
