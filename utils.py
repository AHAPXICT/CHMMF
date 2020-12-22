import numpy as np


def find_y(point_1: list, point_2: list, x: float) -> float:
    return -(((point_1[1] - point_2[1]) * x + (point_1[0] * point_2[1] - point_2[0] * point_1[1])) /
             (point_2[0] - point_1[0]))


def reverse_triangle_points(points: list) -> list:
    """Format triangle points counterclockwise"""

    point_1 = points[0]
    point_2 = points[1]
    point_3 = points[2]

    if point_1[0] < point_2[0]:
        if find_y(point_1, point_2, point_3[0]) > point_3[1]:
            return list(reversed(points))
        else:
            return points
    elif point_1[0] > point_2[0]:
        if find_y(point_1, point_2, point_3[0]) > point_3[1]:
            return points
        else:
            return list(reversed(points))
    else:
        if point_1[1] > point_2[1]:
            if point_3[0] > point_1[0]:
                return points
            else:
                return list(reversed(points))
        else:
            if point_3[0] < point_1[0]:
                return points
            else:
                return list(reversed(points))


def contains_number(number: int, arr: list) -> bool:
    for i in arr:
        if number == i:
            return True

    return False


def find_triangle_points(triangle_number: int, triangles, all_points: list) -> list:
    points_numbers = []
    triangle_points = []

    for edge in triangles:
        if edge[0] == triangle_number:
            points_numbers.append(edge[1])
            points_numbers.append(edge[2])
            points_numbers.append(edge[3])

    for point in all_points:
        if contains_number(point[0], points_numbers):
            triangle_points.append([point[1], point[2]])

    return list(reverse_triangle_points(triangle_points))


def matrix_normalization(k):
    result = np.array(([k.item(0), k.item(1), k.item(2)],
                       [k.item(3), k.item(4), k.item(5)],
                       [k.item(6), k.item(7), k.item(8)]))
    # print(f"normalization: {result}")
    return result


def find_numbers(str):
    point_number = 0
    point_coord_x = 0
    point_coord_y = 0
    i = 0
    while str[i] == '' or str[i] == ' ':
        i+=1

    temp_str = ''
    while str[i] != ' ':
        temp_str += str[i]
        i += 1
    point_number = int(temp_str)

    temp_str = ''
    i += 4
    while str[i] != ' ':
        temp_str += str[i]
        i += 1
    point_coord_x = float(temp_str)

    i += 2
    temp_str = ''
    while str[i] != ' ':
        temp_str += str[i]
        i += 1
    point_coord_y = float(temp_str)
    return point_number, point_coord_x, point_coord_y
    # print(f'point {point_number}: {point_coord_x} {point_coord_y}')


def get_point_by_coords(coords):
    points = []
    temp_arr = []
    file = open('Model/_triangle.1.node', 'r')
    for line in file:
        temp_arr.append(line)
    temp_arr.pop(0)
    temp_arr.pop(-1)
    for i in temp_arr:
        point_number, point_coord_x, point_coord_y = find_numbers(i)
        points.append([point_number, point_coord_x, point_coord_y])
    # print(temp_arr)
    # print(points)
    point = 0
    for i in points:
        if i[1] == coords[0] and i[2] == coords[1]:
            point = i[0]
    # print(point)
    return point


def remove_repeated_lists(arr: list):
    new_arr = []
    for i in arr:
        if i not in new_arr:
            new_arr.append(i)
    return new_arr


remove_repeated_lists([[1, 2], [1, 2], [1, 1]])

# get_point_by_coords([0.5, 1.0])
# find_numbers('  20    0.6728515625  0.4228515625    0')
