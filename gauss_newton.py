from linear_algebra import LinearAlgebra


class GaussNewton(object):
    def __init__(self, order, Xin, Yin):
        self.order = order
        self.Xin = Xin
        self.Yin = Yin

        self.data_size = len(Xin)
        self.iteration_cnt = 100
        self.init_cnt = 0

    def get_jacobian_matrix(self, coeff, expr, symbol_list, variable):
        """
        input: list of coeffcient
        :return: A = [partial differentiation of Xin wrt a0 and a1] mxn
        """
        jacobian_matrix = []
        d = {}
        for c, s in zip(coeff, symbol_list):
            d[s] = c
        for size in range(self.data_size):
            row = []
            d[variable] = self.Xin[size]
            for i in range(len(coeff)):
                part_diff = (expr.diff(symbol_list[i])).subs(d)
                row.append(part_diff)
            jacobian_matrix.append(row)
        return jacobian_matrix

    def get_residue_matrix(self, coeff, expr, symbol_list, variable):
        """
        :return: [Yin-f(Xin)]mxn
        """
        residue_matrix = []
        d = {}
        for c, s in zip(coeff, symbol_list):
            d[s] = c
        for xin,yin in zip(self.Xin, self.Yin):
            d[variable] = xin
            residue_matrix.append([yin-expr.subs(d)])

        return residue_matrix

    def get_coefficient_matrix(self, A, B):
        """
        For input A and B matrix, compute Z which is coefficient of matrix
        A^T*A*Z = A^T*B
        :return: [a0, a1]
        """
        algebra_obj = LinearAlgebra(self.data_size)
        AT = algebra_obj.getTranspose(A, len(A), self.order)
        return algebra_obj.getMultiplication(algebra_obj.getMatrixInverse(algebra_obj.getMultiplication(AT, A)),
                                             algebra_obj.getMultiplication(AT, B))

    def gauss_newton_method(self, init_coeff, expr, symbol_list, variable):
        A = self.get_jacobian_matrix(init_coeff, expr, symbol_list, variable)
        B = self.get_residue_matrix(init_coeff, expr, symbol_list, variable)
        coefficient = self.get_coefficient_matrix(A, B)
        curr_coeff = [round(coefficient[i][0]+init_coeff[i], 2) for i in range(self.order)]
        # print 'Coeffieicnt:', init_coeff, curr_coeff
        termination = True
        for i in range(self.order):
            if abs(init_coeff[i]-curr_coeff[i]) > 0.1:
            #if init_coeff[i] != curr_coeff[i]:
                termination = False
        if termination is True or self.init_cnt == self.iteration_cnt:
            return curr_coeff
        self.init_cnt = self.init_cnt + 1
        return self.gauss_newton_method(curr_coeff, expr, symbol_list, variable)
