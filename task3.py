import numpy as np


def calculate_a_matrix(K, M):
    A = K + M
    return A


print(calculate_a_matrix( np.array(([3,1],[6,4])), np.array(([1,8],[4,2]))))
print(calculate_a_matrix(np.matrix('3 1; 6 4'), np.matrix('1 8; 4 2')))
