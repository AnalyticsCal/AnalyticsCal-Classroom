def get_A_matrix(X):
    index = -1
    A = []
    order = len(X)
    for k in X:
        row = []
        for cnt in range(0, order):
            print (index, cnt)
            row.append(sum(i*j for i,j in zip(X[index], X[cnt])))
        index = index + 1
        A.append(row)
    return A


def get_B_matrix(X, Y):
    index = -1
    B = []
    for k in X:
        B.append(sum(i*j for i,j in zip(Y, X[index])))
        index = index+1
    return B


"""
[[X1, X2, X3, n       ] 
[X1^2, X1X2, X1X3, X1]
[X1X2, X2^2, X2X3, X2]
[X1X3, X2X3, X3^2, X3]]
*
[m3, m2, m1, c]
= 
[Y, YX1, YX2, YX3
]
-> A * coefficient = B

returns: coefficient: [c, m1, m2, m3] 
"""

"""
Sample Data Set - 1
Y = [78, 104, 109, 102, 74, 93, 115, 83, 113, 109]
X1 = [7, 11, 11, 3, 2, 3, 21, 1, 11, 10]
X2 = [26, 52, 55, 71, 31, 54, 47, 40, 66, 68]
X3 = [60, 20, 22, 6, 44, 22, 26, 34, 12, 14]
order = 4
X = [X1, X2, X3]
"""
"""
Sample Data Set - 2
"""

"""
Y = [1.146,-2.443,1.497,-0.132,2.025,0.737,-1.023,-0.956,0.385,0.983,5.092,3.649,2.703,-0.271,2.055,-0.714,0.653,-0.034,-1.058,-2.051,1.451,-0.989,1.358,0.746,1.855,-1.894,0.781,-0.161,2.233,2.425,2.169,0.982,4.708,6.063,9.382,9.304,10.69,6.531,7.873,3.882,4.96,1.301,1.154,0.116,4.928,2.53,8.425,5.291,5.192,0.257,4.402,3.173,5.104,]
X1 = [5.94,6,6.08,6.17,6.14,6.09,5.87,5.84,5.99,6.12,6.42,6.48,6.52,6.64,6.75,6.73,6.89,6.98,6.98,7.1,7.19,7.29,7.65,7.75,7.72,7.67,7.66,7.89,8.14,8.21,8.05,7.94,7.88,7.79,7.41,7.18,7.15,7.27,7.37,7.54,7.58,7.62,7.58,7.48,7.35,7.19,7.19,7.11,7.16,7.22,7.36,7.34,7.3]
X2 = [5.31,5.6,5.49,5.8,5.61,5.28,5.19,5.18,5.3,5.23,5.64,5.62,5.67,5.83,5.53,5.76,6.09,6.52,6.68,7.07,7.12,7.25,7.85,8.02,7.87,7.14,7.2,7.59,7.74,7.51,7.46,7.09,6.82,6.22,5.61,5.48,4.78,4.14,4.64,5.52,5.95,6.2,6.03,5.6,5.26,4.96,5.28,5.37,5.53,5.72,6.04,5.66,5.75]
X3 = [0.29,-0.11,0.31,-0.19,-0.33,-0.09,-0.01,0.12,-0.07,0.41,-0.02,0.05,0.16,-0.3,0.23,0.33,0.43,0.16,0.39,0.05,0.13,0.6,0.17,-0.15,-0.73,0.06,0.39,0.15,-0.23,-0.05,-0.37,-0.27,-0.6,-0.61,-0.13,-0.7,-0.64,0.5,0.88,0.43,0.25,-0.17,-0.43,-0.34,-0.3,0.32,0.09,0.16,0.19,0.32,-0.38,0.09,0.07]
order = 4

X = [X1, X2, X3]
"""
"""
Sample Data Set - 3
Y = [100, 90, 80, 70, 60]
X1 = [110, 120, 100, 90, 80]
X2 = [40, 30, 20, 0, 10]
order = 3
X = [X1, X2]
"""
#X.append([1] * len(X1))

#A = get_A_matrix(X)
#B = get_B_matrix(X)

#print (A)
#print (B)

import linear_algebra

def multi_linear_regression(X, Y):
    order = len(X)+ 1
    print('order before matrix op',order)
    print('X = ',X)

    X.append([1] * len(Y))
    A = get_A_matrix(X)
    B = get_B_matrix(X, Y)
    print ('A = ',A)
    print ('B = ',B)
    matrix_operation = linear_algebra.LinearAlgebra(order)
    inverse = matrix_operation.getMatrixInverse(A)
    coefficient_list = matrix_operation.getMatrixMultiplication(inverse, B)
    coefficient = [coefficient_list[order-1]]+coefficient_list[0:order-1]
    print (coefficient)
    return coefficient
