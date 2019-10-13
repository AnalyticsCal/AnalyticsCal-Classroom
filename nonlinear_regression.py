from linear_algebra import LinearAlgebra
from gauss_newton import GaussNewton
from sympy import *


class NonLinearRegression(object):
    def __init__(self, Xin, Yin):
        self.Xin = Xin
        self.Yin = Yin

    def polynomial(self, order):
        """
        :param order:
        :return: list of coefficient - [B0, B1, B3 .. etc].
         Length of coefficient list is same as order
        """
        degree_of_x = order
        sigma_X = []
        sigma_XY = []
        x_count = 1
        coefficient_list = []
        algebra_obj = LinearAlgebra(len(self.Xin))

        while x_count <= degree_of_x * 2:
            temp = 0
            for x in self.Xin:
                temp = temp + pow(float(x), x_count)

            sigma_X.append(temp)
            x_count += 1

        y_count = 0
        while y_count <= degree_of_x:
            temp = 0
            number_of_x = 0
            for y in self.Yin:
                temp = temp + float(y) * (pow(float(self.Xin[number_of_x]), y_count))
                number_of_x = number_of_x + 1

            sigma_XY.append(temp)
            y_count += 1

        arr = []

        sigma_X.insert(0, float(len(self.Xin)))

        for i in range(degree_of_x + 1):
            temp = []
            for j in range(degree_of_x + 1):
                temp.append(sigma_X[j + i])
            arr.append(temp)

        N = degree_of_x + 1
        adj = []
        inverse = []

        for i in range(N):
            adj.append([])
            inverse.append([])
            for j in range(N):
                adj[i].append([])
                inverse[i].append([])

        sigma_XY_Transpose = []
        for i in range(N):
            sigma_XY_Transpose.append([])
            for j in range(1):
                sigma_XY_Transpose[i].append(0)

        for i in range(N):
            sigma_XY_Transpose[i][0] = sigma_XY[i]

        print('\n Transpose of different sigma xy \n')
        for transpose in sigma_XY_Transpose:
            print(transpose)
        print('\n')

        print('\n Array after finding and putting x and y values in equations \n')
        for a in arr:
            print(a)
        print('\n')

        algebra_obj.get_adjoint(arr, adj)
        print('\n Array Adjoint \n')
        for adjoint in adj:
            print(adjoint)
        print('\n')

        algebra_obj.get_matrix_inverse(arr, inverse)

        print('\n Inverse of Array after finding x and y values \n')
        for inv in inverse:
            print(inv)
        print('\n')

        for i in range(N):
            coefficient_list.append([])
            for j in range(1):
                coefficient_list[i].append(0)

        for i in range(len(inverse)):
            for j in range(len(sigma_XY_Transpose[0])):
                for k in range(len(sigma_XY_Transpose)):
                    coefficient_list[i][j] += inverse[i][k] * sigma_XY_Transpose[k][j]

        return coefficient_list

    def sinusoidal(self, order):
        """
        :param order:
        :return: list of coefficient - [B0, B1, B3 .. etc].
         Length of coefficient list is same as order
        """
        symbol_list = []
        init_coeff = []

        for i in range(order):
            symbol_list.append(symbols('m{}'.format(i), real=True))

        # initialized the coefficient to default 1.0.
        for i in range(order):
            init_coeff.append(1.0)

        x = symbols('x', real=True)
        gauss_obj = GaussNewton(order, self.Xin, self.Yin)

        model = symbol_list[0] * sin(symbol_list[1] * x + symbol_list[2]) + symbol_list[3]
        coefficient = gauss_obj.gauss_newton_method(init_coeff, model, symbol_list, x)

        return coefficient

    def exponential(self, order):
        """
        :param order:
        :return: list of coefficient - [B0, B1, B3 .. etc].
         Length of coefficient list is same as order
        """
        symbol_list = []
        init_coeff = []

        for i in range(order):
            symbol_list.append(symbols('m{}'.format(i), real=True))

        # initialized the coefficient to default 1.0.
        for i in range(order):
            init_coeff.append(1.0)

        x = symbols('x', real=True)
        gauss_obj = GaussNewton(order, self.Xin, self.Yin)

        model = symbol_list[0] * (1.0 - exp(-symbol_list[1] * x))

        coefficient = gauss_obj.gauss_newton_method(init_coeff, model, symbol_list, x)

        return coefficient

    def polynomial_using_gauss_newton(self, order):
        symbol_list = []
        init_coeff = []

        for i in range(order):
            symbol_list.append(symbols('m{}'.format(i), real=True))

        # initialized the coefficient to default 1.0.
        for i in range(order):
            init_coeff.append(1.0)

        x = symbols('x', real=True)
        gauss_obj = GaussNewton(order, self.Xin, self.Yin)

        model = symbol_list[0]
        for order in range(1, order):
            model = model + symbol_list[order] * x ** order

        coefficient = gauss_obj.gauss_newton_method(init_coeff, model, symbol_list, x)

        return coefficient

    def power(self, order):
        """
        :param order:
        :return: list of coefficient - [B0, B1, B3 .. etc].
         Length of coefficient list is same as order
        """
        pass
