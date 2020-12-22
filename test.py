import numpy as np


matrix_3_3 = np.matrix(
    f'1; 2; 3; '
    f'4; 5; 6; '
    f'7; 8; 9'
)

matrix_3_1 = np.matrix(
    f'2; '
    
    f'2; '
    f'2'
)

t = np.matmul(matrix_3_3, matrix_3_1)
print(t)
