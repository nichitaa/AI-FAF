import math


# 2D vector normalization
def v_norm_2d(v):
    length = math.sqrt(v[0] ** 2 + v[1] ** 2)
    return [v[0] / length, v[1] / length]


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
    return [v[0] / scalar, v[1] / scalar]


# 2D vectors dot product
def v_dot_2d(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]
