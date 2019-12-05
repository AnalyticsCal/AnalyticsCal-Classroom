from linear_algebra import LinearAlgebra
from gauss_newton import GaussNewton


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
        algebra_obj.N = N
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


        # clean up the coefficient list
        return [coefficient[0] for coefficient in coefficient_list]
        #return coefficient_list

    def sinusoidal(self, order):
        """
        :param order:
        :return: list of coefficient - [B0, B1, B3 .. etc].
         Length of coefficient list is same as order
        """

        # check the order
        if order != 4:
            return 'Permissible valued of order for sinusoidal model is 4'

        from sympy import symbols,sin

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
        # check the order
        if order != 2:
            return 'Permissible valued of order for sinusoidal model is 2'

        from sympy import symbols, exp

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
        from sympy import symbols

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
    
    def exponentialTransformation(self, order):
        """
            :param order:
            :return: list of coefficient - [B0, B1].
             Length of coefficient list is same as order
        """
        print('Inside exp')
        # check the order
        if order != 1:
            return 'Permissible value for order in exponentialTransformation model is 1'

        # below method returns number after decimal point
        def num_after_point(a): #a is float or string value
            s = str(a)
            if not '.' in s:
                return 0
            return len(s) - s.index('.') - 1

        import numpy
        #import linearRegression

        num_after_decimal = num_after_point(self.Yin[0])
        #Convert Yin into LogYin with round upto decimal as input values
        lnYin = [round(numpy.log(float(y)),num_after_decimal) for y in self.Yin]

        #round Xin values upto decimal same as input values
        round_Xin = [round(float(x),num_after_decimal) for x in self.Xin]

        #Call linearRegression function here--------------
        self.Xin = round_Xin
        self.Yin = lnYin
        coefficient1 = self.polynomial(1)

        coefficient_list = []
        i = 0
        for coeff in coefficient1:
            if i == 0:
                #convert B0 to original form
                coefficient_list.append(round(numpy.exp(float(coeff)),num_after_decimal)) 
                i += 1
            else:
                coefficient_list.append(round(float(coeff),num_after_decimal))

        return coefficient_list

    #Nonlinear to linear transformation using scaling factor
    #For scaling negative data points in the dataset (Xin,Yin)
    def findMin(inp):
        min = 0
        for i in inp:
            if i < min and i < 0:
                min = i
        return min

    def scaleFactor(Xin,Yin):
        if len(x)==len(y):
            xMin = findMin(Xin)
            yMin = findMin(Yin)
            k = xMin
            if yMin<xMin:
                k = yMin
            return mod_number(k)
        return 0
    
    def mod_number(x):
        if x < 0:
            strVal = str(x)
            substrVal = strVal[1:]
            return int(substrVal)
        return 0

    def applyScaleFactorToDataPoints():
        k = scaleFactor(x,y)
        #print('Scale Factor:',k)
        if k > 0:
            i=0;
            while i < len(x):
                self.Xin[i]+=k
                i+=1
            #print(self.Xin)
            i=0
            while i < len(y):
                self.Yin[i]+=k
                i+=1
            #print(self.Yin)
