import numpy as np
from math import sqrt


def find_side_len(point_1: list, point_2: list) -> float:
    return sqrt(((point_2[0] - point_1[0])**2 + (point_2[1] - point_1[1])**2))


def find_sides(point_i: list, point_j: list, point_m: list) -> list:
    sides = []
    side_i_j = sqrt(np.power((point_j[0] - point_i[0]), 2) +
                    np.power((point_j[1] - point_i[1]), 2))

    side_j_m = sqrt(np.power((point_m[0] - point_j[0]), 2) +
                    np.power((point_m[1] - point_j[1]), 2))

    side_m_i = sqrt(np.power((point_i[0] - point_m[0]), 2) +
                    np.power((point_i[1] - point_m[1]), 2))

    sides.append(side_i_j)
    sides.append(side_j_m)
    sides.append(side_m_i)

    return sides


def find_triangle_square(point_1: list, point_2: list, point_3: list) -> float:
    matrix = np.matrix(f'1 {point_1[0]} {point_1[1]}; '
                       f'1 {point_2[0]} {point_2[1]}; '
                       f'1 {point_3[0]} {point_3[1]}'
                       )

    square = np.linalg.det(matrix)

    return square


def find_phi(point_p: list, point_i: list, point_j: list, point_m: list) -> float:
    s_p_j_m = find_triangle_square(point_p, point_j, point_m)
    s_i_j_m = find_triangle_square(point_i, point_j, point_m)

    print("s_p_j_m: ", s_p_j_m)
    print("s_i_j_m: ", s_i_j_m)

    phi = s_p_j_m / s_i_j_m

    return phi


find_phi(
    point_p=[0.1, 0.1],
    point_i=[0, 0],
    point_j=[1, 0],
    point_m=[0, 1])


def find_m(d: float, delta: float) -> list:
    matrix = np.matrix(
        f'2 1 1; '
        f'1 2 1; '
        f'1 1 2'
    )

    m_e = ((d * delta) / 24) * matrix

    return m_e


def find_r(border: float, betta: float, sigma: float) -> list:
    matrix = np.matrix(
        f'2 1; '
        f'1 2'
    )

    r_e = ((border * sigma) / (6 * betta)) * matrix

    return r_e


def find_b(point_1: list, point_2: list, point_3: list) -> list:
    y_array = [point_1[1], point_2[1], point_3[1], point_1[1], point_2[1], point_3[1]]

    b = []

    for i in range(3):
        b.append(y_array[i + 1] - y_array[i + 2])

    return b


def find_c(point_1: list, point_2: list, point_3: list) -> list:
    x_array = [point_1[0], point_2[0], point_3[0], point_1[0], point_2[0], point_3[0]]

    c = []

    for i in range(3):
        c.append(x_array[i + 2] - x_array[i + 1])

    return c


def find_a(point_1: list, point_2: list, point_3: list) -> list:
    x_array = [point_1[0], point_2[0], point_3[0], point_1[0], point_2[0], point_3[0]]
    y_array = [point_1[1], point_2[1], point_3[1], point_1[1], point_2[1], point_3[1]]

    a = []

    for i in range(3):
        a[i] = (x_array[i + 1] * y_array[i + 2]) - (x_array[i + 2] * y_array[i + 1])

    return a


def find_k(square: float, a_1_1: float, a_2_2: float, b: list, c: list, trian):
    b_i = trian[1][1] - trian[2][1]
    b_j = trian[2][1] - trian[0][1]
    b_m = trian[0][1] - trian[1][1]
    c_i = trian[2][0] - trian[1][0]
    c_j = trian[0][0] - trian[2][0]
    c_m = trian[1][0] - trian[0][0]
    # print("iter b", b_i,b_j,b_m)
    # print("iter c",c_i,c_j,c_m)
    # count matrix Ke
    el_00 = a_1_1 * b_i ** 2 + a_2_2 * c_i ** 2
    el_11 = a_1_1 * b_j ** 2 + a_2_2 * c_j ** 2
    el_22 = a_1_1 * b_m ** 2 + a_2_2 * c_m ** 2

    el_01 = a_1_1 * b_i * b_j + a_2_2 * c_i * c_j
    el_02 = a_1_1 * b_i * b_m + a_2_2 * c_i * c_m
    el_12 = a_1_1 * b_j * b_m + a_2_2 * c_j * c_m
    matrix_Ke = [[el_00, el_01, el_02], [el_01, el_11, el_12], [el_02, el_12, el_22]]

    Ke = np.dot((1.0 / (square ** 2)), matrix_Ke)

    # matrix = np.matrix(
    #     f'{(a_1_1 * b[0] ** 2) + (a_2_2 * c[0] ** 2)}; {(a_1_1 * b[0] * b[1]) + (a_2_2 * c[0] * c[1])}; {(a_1_1 * b[0] * b[2]) + (a_2_2 * c[0] * c[2])}; '
    #     f'{(a_1_1 * b[0] * b[1]) + (a_2_2 * c[0] * c[1])}; {(a_1_1 * b[1] * b[1]) + (a_2_2 * c[1] * c[1])}; {(a_1_1 * b[1] * b[2]) + (a_2_2 * c[1] * c[2])}; '
    #     f'{(a_1_1 * b[0] * b[2]) + (a_2_2 * c[0] * c[2])}; {(a_1_1 * b[1] * b[2]) + (a_2_2 * c[1] * c[2])}; {(a_1_1 * b[2] * b[2]) + (a_2_2 * c[2] * c[2])}'
    # )
    #
    # k = matrix / (4*(square**2))

    return Ke


def find_q(m_e: list) -> list:
    # if d == 0:
    #     d = 0.00000000001

    f = [1, 1, 1]
    d = 1

    t2 = m_e.item((0, 0))

    q_e = np.dot((m_e / d), f)

    return q_e


def find_p(border: float, betta: float, ksi: float, sigma: float) -> list:
    p = np.matrix(f'{(ksi * border * sigma ) / (2 * betta)}; '
                  f'{(ksi * border * sigma )/ (2 * betta)}')

    return p
