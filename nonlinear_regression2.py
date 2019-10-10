from sympy import *
from linear_algebra import *
from config import *
"""
Y = a0*(1-e^(-a1*X))
Calculate a0, a1 using Gauss Newton
"""
Xin = [0.25, 0.75, 1.25, 1.75, 2.25]
Yin = [0.28, 0.57, 0.68, 0.74, 0.79]
data_size = len(Xin)

def get_jacobian_matrix(coeff, expr, symbol_list):
    """
    input: list of coeffcient
    :return: A = [partial differentiation of Xin wrt a0 and a1] mxn
    """
    jacobian_matrix = []
    d = {}
    for c, s in zip(coeff, symbol_list):
        d[s] = c
    for size in range(data_size):
        row = []
        d[x] = Xin[size]
        for i in range(len(coeff)):
            part_diff = (expr.diff(symbol_list[i])).subs(d)
            row.append(part_diff)
        jacobian_matrix.append(row)
    return jacobian_matrix


def get_residue_matrix(coeff, expr, symbol_list):
    """
    :return: [Yin-f(Xin)]mxn
    """
    residue_matrix = []
    d = {}
    for c, s in zip(coeff, symbol_list):
        d[s] = c
    for xin,yin in zip(Xin, Yin):
        d[x] = xin
        residue_matrix.append([yin-expr.subs(d)])

    return residue_matrix


def get_coefficient_matrix(A, B):
    """
    For input A and B matrix, compute Z which is coefficient of matrix
    A^T*A*Z = A^T*B
    :return: [a0, a1]
    """
    AT = getTranspose(A, len(A), order)
    return getMultiplication(getMatrixInverse(getMultiplication(AT, A)), getMultiplication(AT, B))


def gauss_newton_method(init_coeff, init_cnt, expr, symbol_list):
    A = get_jacobian_matrix(init_coeff, expr, symbol_list)
    B = get_residue_matrix(init_coeff, expr, symbol_list)
    print 'A:', A
    print 'B:', B
    coefficient = get_coefficient_matrix(A, B)
    #print coefficient
    coeff_size = len(init_coeff)
    curr_coeff = [round(coefficient[i][0]+ init_coeff[i], 2) for i in range(coeff_size)]

    #print 'cnt', init_cnt
    #print 'Coeffieicnt:', curr_coeff
    termination = True
    for i in range(coeff_size):
        if init_coeff[i] != curr_coeff[i]:
            termination = False

    if termination is True or  init_cnt == iteration_cnt:
        return curr_coeff
    init_cnt = init_cnt + 1
    #return
    gauss_newton_method(curr_coeff, init_cnt, expr, symbol_list)
    return curr_coeff


coeffieicnt = gauss_newton_method(init_coeff, init_cnt, expr, symbol_list)
print coeffieicnt
