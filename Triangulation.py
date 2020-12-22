import warnings
import numpy as np
from flopy.utils.triangle import Triangle as Triangle
import matplotlib.pyplot as plt

from task2 import find_triangle_square, find_a, find_b, find_c, find_k, find_m, find_r, find_side_len, find_p, find_q
from task3 import calculate_a_matrix
from utils import find_triangle_points, contains_number, matrix_normalization, get_point_by_coords, \
    remove_repeated_lists, find_numbers

# G_3 = [10 ** 5, 10 ** (-5), 0] #betta, sigma, ksi
# G_1 = [10 ** 5, 10 ** (-5), 0]
# G_4 = [10 ** (-5), 10**5, 0]
# G_1 = G_3 = G_4 =
G_1 = G_3 = G_4 = G_2 = [10 ** (-5), 10**5, 0]


def get_numbers(line):
    l = len(line)
    integ = []
    i = 0
    while i < l:
        line_int = ''
        a = line[i]
        while '0' <= a <= '9':
            line_int += a
            i += 1
            if i < l:
                a = line[i]
            else:
                break
        i += 1
        if line_int != '':
            integ.append(int(line_int))
    return integ


points = [(0, 0), (1, 0), (1, 1), (0, 1)]

workspace = './Model/'
triExeName = './EXE/triangle.exe'

tri = Triangle(model_ws=workspace, exe_name=triExeName, maximum_area=0.002)
tri.add_polygon(points)
tri.build()

fig = plt.figure(figsize=(15, 15))
ax = plt.subplot(1, 1, 1, aspect='equal')
tri.plot(ax=ax, edgecolor='gray')
tri.plot_vertices(ax=ax, marker='o', color='blue')
tri.label_vertices(ax=ax, fontsize=40, color='blue')
tri.plot_centroids(ax=ax, marker='o', color='red')
tri.label_cells(ax=ax, fontsize=40, color='red')

# for i in tri.get_vertices():
#     print(f"{i[0]} point have: {round(i[1], 3)}"
#           f" {round(i[2], 3)} coords")

triangles = []

ele_file = open('Model/_triangle.1.ele', 'r')
for line in ele_file:
    triangles.append(get_numbers(line))
triangles.remove(triangles[0])
triangles.pop()

edge_file = open('Model/_triangle.1.edge', 'r')

edges = []

for line in edge_file:
    if len(get_numbers(line)) >= 4 and get_numbers(line)[3] != 0:
        edges.append(get_numbers(line))

values = set(map(lambda x: x[3], edges))
edges = [[[edge[1], edge[2]] for edge in edges if edge[3] == x] for x in values]

# for edge in edges:
#     print(f"{edge}\n")

for i in range(len(triangles)):
    print(f'for triangle {i + 1}:  {find_triangle_points(i, triangles, tri.get_vertices())}')


def print_matrix_3_x_3(matrix: list) -> None:
    k = 0
    for elem in range(3):
        print(f'{matrix[k]}, {matrix[k + 1]}, {matrix[k + 2]}')
        k += 3


print()
print(
    '======================================================================================================================================')
print()

k = 0

k_martrix_array = []
m_martrix_array = []
q_matrix_array = []

for i in range(len(triangles)):
    test_triangle_points = find_triangle_points(i, triangles, tri.get_vertices())

    triangle_square = find_triangle_square(test_triangle_points[0],
                                           test_triangle_points[1],
                                           test_triangle_points[2])

    b_for_k = find_b(test_triangle_points[0],
                     test_triangle_points[1],
                     test_triangle_points[2])

    c_for_k = find_c(test_triangle_points[0],
                     test_triangle_points[1],
                     test_triangle_points[2])

    a_1_1 = 1
    a_2_2 = 1

    trian = []
    trian.append(test_triangle_points[0])
    trian.append(test_triangle_points[1])
    trian.append(test_triangle_points[2])

    print(test_triangle_points[0])
    print(test_triangle_points[1])
    print(test_triangle_points[2])

    k_matrix = find_k(square=triangle_square,
                      a_1_1=a_1_1,
                      a_2_2=a_2_2,
                      b=b_for_k,
                      c=c_for_k,
                      trian=trian)

    k_matrix = matrix_normalization(k_matrix)

    print(f'For triangle {k + 1} matrix K: ')
    # print_matrix_3_x_3(k_matrix)
    print(k_matrix)
    print(f'shape K matrix: {k_matrix.shape}')
    print(type(k_matrix))
    print()
    print()


    # print(f'shape new K matrix: {new_k_matrix.shape}')



    print(f'For triangle {k + 1} matrix M: ')
    m_matrix = find_m(1, triangle_square)
    print(m_matrix)
    print(f'shape M matrix: {m_matrix.shape}')
    print(type(m_matrix))
    print()
    print()



    # print("A matrix: ")
    # print(calculate_a_matrix(k_matrix, m_matrix))
    # print("\n\n")

    q_matrix = find_q(m_matrix)

    print(f'For triangle {k + 1} matrix Q: ')
    print(q_matrix)
    print('\n\n')

    k += 1

    k_martrix_array.append(k_matrix)
    m_martrix_array.append(m_matrix)
    q_matrix_array.append(q_matrix)



test_triangle_points = [[1.0, 1.0], [0.5, 0.5], [1.0, 0.5]]


def find_coord_by_number(points, number):
    result = []
    for i in points:
        if i[0] == number:
            result.append(i[1])
            result.append(i[2])
            return result

print(find_coord_by_number([[1, 2, 3], [2, 3, 3]], 1))


def remove_repeated_elements(arr):
    new_arr = []
    for i in range(len(arr)):
        # k = 0
        if arr[i] in new_arr:
            continue
        else:
            new_arr.append(arr[i])

    return new_arr


def find_points_number_on_border(points_coords):
    points = []
    poly_file = open('Model/_triangle.1.poly', 'r')
    for line in poly_file:
        if len(get_numbers(line)) >= 4 and get_numbers(line)[3] != 0:
            points.append(get_numbers(line))

    # for i in points:
    #     i.pop(0)

    points.pop(0)

    new_points = []

    border_1 = []
    border_2 = []
    border_3 = []
    border_4 = []

    for i in points:
        if i[3] == 1:
            border_1.append(i)
        elif i[3] == 2:
            border_2.append(i)
        elif i[3] == 3:
            border_3.append(i)
        elif i[3] == 4:
            border_4.append(i)


    new_border_1 = list(reversed(border_1))
    new_border_2 = list(reversed(border_2))
    new_border_3 = list(reversed(border_3))
    new_border_4 = list(reversed(border_4))

    new_points = new_border_1 + new_border_2 + new_border_3 + new_border_4

    return new_points


def find_points_on_border(points_coords):
    points = []
    poly_file = open('Model/_triangle.1.poly', 'r')
    for line in poly_file:
        if len(get_numbers(line)) >= 4 and get_numbers(line)[3] != 0:
            points.append(get_numbers(line))

    for i in points:
        i.pop(0)

    border_1 = []
    border_2 = []
    border_3 = []
    border_4 = []
    for i in points_coords:
        print(f'{i[0]} {i[1]} {i[2]}', '\n')

    points.pop(0)

    for i in points:
        if i[2] == 1:
            border_1.append(find_coord_by_number(points_coords, i[0]))
            border_1.append(find_coord_by_number(points_coords, i[1]))
        elif i[2] == 2:
            border_2.append(find_coord_by_number(points_coords, i[0]))
            border_2.append(find_coord_by_number(points_coords, i[1]))
        elif i[2] == 3:
            border_3.append(find_coord_by_number(points_coords, i[0]))
            border_3.append(find_coord_by_number(points_coords, i[1]))
        elif i[2] == 4:
            border_4.append(find_coord_by_number(points_coords, i[0]))
            border_4.append(find_coord_by_number(points_coords, i[1]))



    new_border_1 = list(remove_repeated_elements(border_1))
    new_border_2 = list(remove_repeated_elements(border_2))
    new_border_3 = list(remove_repeated_elements(border_3))
    new_border_4 = list(remove_repeated_elements(border_4))

    print('\n\n')

    print("new border 1: ", list(reversed(new_border_1)))
    print("new border 2: ", list(reversed(new_border_2)))
    print("new border 3: ", list(reversed(new_border_3)))
    print("new border 4: ", list(reversed(new_border_4)))

    new_border_1 = list(reversed(new_border_1))
    new_border_2 = list(reversed(new_border_2))
    new_border_3 = list(reversed(new_border_3))
    new_border_4 = list(reversed(new_border_4))

    return new_border_1, new_border_2, new_border_3, new_border_4

    # print(points)



r_matrix_1 = find_r(find_side_len([1, 1], [0, 1]), G_1[0], G_1[1])
r_matrix_2 = find_r(find_side_len([0, 1], [0, 0]), G_2[0], G_2[1])
r_matrix_3 = find_r(find_side_len([0, 0], [1, 0]), G_3[0], G_3[1])
r_matrix_4 = find_r(find_side_len([1, 0], [1, 1]), G_4[0], G_4[1])

# print(f'matrix R1:\n {r_matrix_1} \n\n')
# print(f'matrix R2:\n {r_matrix_2} \n\n')
# print(f'matrix R3:\n {r_matrix_3} \n\n')
# print(f'matrix R4:\n {r_matrix_4} \n\n')





p_matrix_1 = find_p(find_side_len([1, 1], [0, 1]), G_1[0], G_1[2], G_1[1])
p_matrix_2 = find_p(find_side_len([0, 1], [0, 0]), G_2[0], G_2[2], G_1[1])
p_matrix_3 = find_p(find_side_len([0, 0], [1, 0]), G_3[0], G_3[2], G_1[1])
p_matrix_4 = find_p(find_side_len([1, 0], [1, 1]), G_4[0], G_4[2], G_1[1])


# print(f'matrix P1:\n {p_matrix_1} \n\n')
# print(f'matrix P2:\n {p_matrix_2} \n\n')
# print(f'matrix P3:\n {p_matrix_3} \n\n')
# print(f'matrix P4:\n {p_matrix_4} \n\n')

border_1, border_2, border_3, border_4 = find_points_on_border(tri.get_vertices())
border_points = border_1 + border_2 + border_3 + border_4

k = 1

r_matrix_array = []
p_matrix_array = []

print("For border 1: \n\n")
print(border_1)
for i in range(len(border_1) - 1):
    r_matrix = find_r(find_side_len(border_1[i], border_1[i + 1]), G_1[0], G_1[1])
    p_matrix = find_p(find_side_len(border_1[i], border_1[i + 1]), G_1[0], G_1[2], G_1[1])
    r_matrix_array.append(r_matrix)
    p_matrix_array.append(p_matrix)
    print(f'matrix R{k}:\n {r_matrix} \n\n')
    print(f'matrix P{k}:\n {p_matrix} \n\n')
    k += 1


print("For border 2: \n\n")
for i in range(len(border_2) - 1):
    r_matrix = find_r(find_side_len(border_2[i], border_2[i + 1]), G_2[0], G_2[1])
    p_matrix = find_p(find_side_len(border_2[i], border_2[i + 1]), G_2[0], G_2[2], G_2[1])
    r_matrix_array.append(r_matrix)
    p_matrix_array.append(p_matrix)
    print(f'matrix R{k}:\n {r_matrix} \n\n')
    print(f'matrix P{k}:\n {p_matrix} \n\n')
    k += 1

print("For border 3: \n\n")
for i in range(len(border_3) - 1):
    r_matrix = find_r(find_side_len(border_3[i], border_3[i + 1]), G_3[0], G_3[1])
    p_matrix = find_p(find_side_len(border_3[i], border_3[i + 1]), G_3[0], G_3[2], G_3[1])
    r_matrix_array.append(r_matrix)
    p_matrix_array.append(p_matrix)
    print(f'matrix R{k}:\n {r_matrix} \n\n')
    print(f'matrix P{k}:\n {p_matrix} \n\n')
    k += 1

print("For border 4: \n\n")
for i in range(len(border_4) - 1):
    r_matrix = find_r(find_side_len(border_4[i], border_4[i + 1]), G_4[0], G_4[1])
    p_matrix = find_p(find_side_len(border_4[i], border_4[i + 1]), G_4[0], G_4[2], G_4[1])
    r_matrix_array.append(r_matrix)
    p_matrix_array.append(p_matrix)
    print(f'matrix R{k}:\n {r_matrix} \n\n')
    print(f'matrix P{k}:\n {p_matrix} \n\n')
    k += 1


print("count: ")
node_file = open('Model/_triangle.1.node', 'r')
count_nodes = get_numbers(node_file.readline())[0]
print(count_nodes)

A = np.zeros((count_nodes, count_nodes))
A1 = np.zeros((count_nodes, count_nodes))
# print(A)

# [0, 2, 5, 7]

file = open("matrix.txt", "w")
file1 = open("matrix1.txt", "w")
for triangle in triangles:
    # print(f"triangles {triangle}\n")
    # print(k_martrix_array[triangle[0]][0].tolist())
    for i in range(1, 4):
        for j in range(1, 4):
            A1[triangle[i], triangle[j]] += k_martrix_array[triangle[0]].tolist()[i-1][j-1] + m_martrix_array[triangle[0]].tolist()[i-1][j-1]
############################################################

for i in range(0, count_nodes):
    for j in range(0, count_nodes):
        file1.write(str(A1[i][j]) + '    ')
    file1.write('\n')


#############################################################
# print(r_matrix_array[0])
# #
# border_points = find_points_number_on_border(tri.get_vertices())
# for p in border_points:
#     for i in range(0, 2):
#         for j in range(0, 2):
#             # print(A[border_points[i+1], border_points[j+1]])
#             A[border_points[i+1], border_points[j+1]] += r_matrix_array[p[0]].tolist()[i][j]
#
#             # print(A[border_points[i+1], border_points[j+1]])
#             # print('\n\n')
#
#             # print(r_matrix_array[p[0]].tolist()[i][j])
#
# for i in range(0, count_nodes):
#     for j in range(0, count_nodes):
#         file.write(str(A[i][j]) + '    ')
#     file.write('\n')
#
#
# b_vector = [0 for i in range(0, A.shape[0])]
#
# print(q_matrix_array[0])
#
#
#
#
# print(len(triangles))
# print(count_nodes)

#############################################################

# [[1,]
# [2]]

# print("################")
# print(len(triangles))
# print(triangles[2])
# # print(b_vector[triangles[2]])

##########################################################
# for triangle in triangles:
#     for j in range(1, 4):
#         b_vector[triangle[j]-1] += q_matrix_array[j].tolist()[0][j-1]
#
# new_b_vector = []
#############################################################


# print('--------------')
# print(p_matrix_array[7])
# print(p_matrix_array[7].item(0))
# print(type(p_matrix_array[7].item(1)))
# print('--------------')
#
# print(border_points)
# print(b_vector)
#
#############################################################
# for p in border_points:
#     for j in range(0, 2):
#         b_vector[p[j+1]] += p_matrix_array[p[0]].item(j)
# #
# #
# for i in range(count_nodes):
#     new_b_vector.append(b_vector[i])
#
# b_vector = new_b_vector
# print(len(b_vector))
# print(b_vector)
# #
# print('----------------------------------------------------------------------------------------------------------')
# print('----------------------------------------------------------------------------------------------------------')
#
# result = np.linalg.solve(A, b_vector)
# print(result)
#
#############################################################
#
# # tem = find_points_on_border(tri.get_vertices())
# # print(tem)
#
#
# # print(f"A: {A[17][17]}")
#

print(triangles) #[0, 7, 2, 4]
m_matrix_test = m_martrix_array[0]
k_martrix_test = k_martrix_array[0]
print(m_matrix_test)
print(k_martrix_test)
triangle_test = triangles[0]
print(m_matrix_test.item(0,0))

B = [0 for i in range(0, A.shape[0])]
# []
print("***********************************************************")

for triangle in triangles:
    for i in range(m_matrix_test.shape[0]):
        for j in range(m_matrix_test.shape[0]):
            m_matrix_t = m_martrix_array[triangle[0]]
            print(m_matrix_t)
            k_matrix_t = k_martrix_array[triangle[0]]
            print(k_matrix_t)
            A[triangle[i + 1]][triangle[j + 1]] += m_matrix_t.item(i, j) + k_matrix_t.item(i, j)

# triangle = [0, 7, 2, 4]
# for i in range(m_matrix_test.shape[0]):
#     for j in range(m_matrix_test.shape[0]):
#         m_matrix_t = m_martrix_array[triangle[0]]
#         print(m_matrix_t)
#         k_matrix_t = k_martrix_array[triangle[0]]
#         print(k_matrix_t)
#         A[triangle[i + 1]][triangle[j + 1]] = m_matrix_t.item(i, j) + k_matrix_t.item(i, j)



for i in range(0, count_nodes):
    for j in range(0, count_nodes):
        file.write(str(A[i][j]) + '    ')
    file.write('\n')



print('====================================================================')
r_matrix_test = r_matrix_array[0]
print(r_matrix_test)

border_items = len(r_matrix_array)
print(border_items)
print('====================================================================')
print(border_points)
border_points = remove_repeated_lists(border_points)
print(border_points)
border_intervals = []
for i in range(len(r_matrix_array) - 1):
    # if i == len(r_matrix_array) - 2:
    #     border_intervals.append([i, get_point_by_coords(border_points[i + 1]), get_point_by_coords(border_points[0])])
    border_intervals.append([i, get_point_by_coords(border_points[i]), get_point_by_coords(border_points[i + 1])])
border_intervals.append([len(r_matrix_array) - 1, get_point_by_coords(border_points[len(r_matrix_array) - 2 + 1]), get_point_by_coords(border_points[0])])

print(border_intervals)
r_matrix_test = r_matrix_array[0]
print(r_matrix_test)

for interval in border_intervals:
    for i in range(r_matrix_test.shape[0]):
        for j in range(r_matrix_test.shape[0]):
            r_matrix_t = r_matrix_array[interval[0]]
            A[interval[i+1]][interval[j+1]] += r_matrix_t.item(i, j)

print('====================================================================')

b_vector = [0 for i in range(0, A.shape[0])]

# b_vector = [ 8.3333e-02,
#  2.5000e+09,
#  2.5000e+09,
#  8.3333e-02,
#  3.3333e-01,
#  8.3333e-02,
#  8.3333e-02,
#  5.0000e+09,
#  8.3333e-02,
# ]

for triangle in triangles:
    for j in range(m_matrix_test.shape[0]):
        q_matrix_t = q_matrix_array[triangle[0]]
        b_vector[triangle[j + 1]] += q_matrix_t.item(0, j)

# triangle = triangles[0]
# for j in range(m_matrix_test.shape[0]):
#         q_matrix_t = q_matrix_array[triangle[0]]
#         b_vector[triangle[j + 1]] = q_matrix_t.item(0, j)

#
for interval in border_intervals:
    for i in range(r_matrix_test.shape[0]):
        p_matrix_t = p_matrix_array[interval[0]]
        b_vector[interval[i + 1]] += p_matrix_t.item(i, 0)

print(b_vector)

result = np.linalg.solve(A, b_vector)
for i in result:
    print(i)
# print(result)

# for border_item in range(border_items):
#     for i in range(m_matrix_test.shape[0]):
#         for j in range(m_matrix_test.shape[0]):
#             m_matrix_t = m_martrix_array[triangle[0]]
#             k_matrix_t = k_martrix_array[triangle[0]]
#             A[triangle[i+1]][triangle[j+1]] = m_matrix_t.item(i, j) + k_matrix_t.item(i, j)

points_for_g_x = []
points_for_g_y = []

for i in tri.get_vertices():
    points_for_g_x.append(i[1])
    points_for_g_y.append(i[2])



# points_for_g_x = [
#     0,
#     1,
#     1,
#     0,
#     0.5,
#     0,
#     0.5,
#     1,
#     0.5
# ]

# points_for_g_y = [
#     0,
#     0,
#     1,
#     1,
#     0.5,
#     0.5,
#     0,
#     0.5,
#     1
# ]
plt3d = plt.figure().gca(projection='3d')
ax = plt.gca()
# ax.hold(True)
# for i in range(9):
#     ax.scatter(points_for_g_x[i], points_for_g_y[i], result[i], color='green')
ax.plot_trisurf(points_for_g_x, points_for_g_y, result, cmap=plt.get_cmap('hot'), antialiased=True)


warnings.filterwarnings("ignore")
plt.show()




# triangle_square = find_triangle_square(test_triangle_points[0],
#                                        test_triangle_points[1],
#                                        test_triangle_points[2])
#
#
#
#
# m_matrix = find_m(1, triangle_square*2)
# print(m_matrix)
# q_matrix = find_q(m_matrix)
# print("q matrix: ", q_matrix)



# def getTriangPoints():
#     coords = []
#     for i in tri.get_vertices():
#         coords.append([i[1], -i[2], f"{i[0]}"])
#     print(coords)
#     return coords
#
#
# def getTriangCenterPoints():
#     coords = []
#     k = 0
#     for i in tri.get_xcyc():
#         coords.append([i[0], -i[1], f"{k}"])
#         k += 1
#     print(coords)
#     return coords
#
#
# def getTrianglePoints():
#     triangles = []
#
#     ele_file = open('Model/_triangle.1.ele', 'r')
#     for line in ele_file:
#         triangles.append(get_numbers(line))
#     triangles.remove(triangles[0])
#     triangles.pop()
#     return triangles
#
#
# def getEdges():
#     edge_file = open('Model/_triangle.1.edge', 'r')
#
#     edges = []
#
#     for line in edge_file:
#         if len(get_numbers(line)) >= 4 and get_numbers(line)[3] != 0:
#             edges.append(get_numbers(line))
#
#     values = set(map(lambda x: x[3], edges))
#     edges = [[[edge[1], edge[2]] for edge in edges if edge[3] == x] for x in values]
#
#     return edges
