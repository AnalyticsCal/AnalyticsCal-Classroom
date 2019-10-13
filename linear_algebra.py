class LinearAlgebra(object):
    def __init__(self, N):
        self.N = N

    @staticmethod
    def get_cofactor(arr, temp, p, q, n):
        i = 0
        j = 0
        for row in range(n):
            for col in range(n):
                if row != p and col != q:
                    temp[i][j] = arr[row][col]
                    j += 1

                    if j == n - 1:
                        j = 0
                        i += 1

    def get_det(self, arr, n):
        D = 0

        if n == 1:
            return arr[0][0]

        temp = []
        for i in range(self.N):
            temp.append([])
            for j in range(self.N):
                temp[i].append([])

        sign = 1

        for f in range(n):
            self.get_cofactor(arr, temp, 0, f, n)
            D += sign * arr[0][f] * self.get_det(temp, n - 1)
            sign = -sign

        return D

    def get_adjoint(self, arr, adj):
        if self.N == 1:
            adj[0][0] = 1
            return

        temp = []
        for i in range(self.N):
            temp.append([])
            for j in range(self.N):
                temp[i].append([])

        for i in range(self.N):
            for j in range(self.N):

                self.get_cofactor(arr, temp, i, j, self.N)

                sign = 1 if ((i + j) % 2 == 0) else -1

                # adj[p][q] = sign * get_matrix_determinant(tmp)
                adj[j][i] = sign * self.get_det(temp, self.N - 1)

    def get_matrix_inverse(self, arr, inverse):
        # determinant = get_matrix_determinant(m)

        determinant = self.get_det(arr, self.N)
        # special case for 2x2 matrix:
        # if len(arr) == 2:
        #    return [[arr[1][1]/determinant, -1*arr[0][1]/determinant],
        #            [-1*arr[1][0]/determinant, arr[0][0]/determinant]]
        # find matrix of co-factors

        adj = []
        for i in range(self.N):
            adj.append([])
            for j in range(self.N):
                adj[i].append([])

        self.get_adjoint(arr, adj)

        for i in range(self.N):
            for j in range(self.N):
                inverse[i][j] = adj[i][j] / float(determinant)

    def transposeMatrix(self, m):
        return map(list, zip(*m))

    def getMatrixMinor(self, m, i, j):
        return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

    def getMatrixDeternminant(self, m):
        # base case for 2x2 matrix
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1) ** c) * m[0][c] * self.getMatrixDeternminant(self.getMatrixMinor(m, 0, c))
        return determinant

    def getMatrixInverse(self, m):
        determinant = self.getMatrixDeternminant(m)
        # special case for 2x2 matrix:
        if len(m) == 2:
            return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                    [-1 * m[1][0] / determinant, m[0][0] / determinant]]

        # find matrix of cofactors
        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMatrixMinor(m, r, c)
                cofactorRow.append(((-1) ** (r + c)) * self.getMatrixDeternminant(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transposeMatrix(cofactors)
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] = cofactors[r][c] / determinant
        return cofactors

    def getMatrixMultiplication(self, m, n):
        mul = []
        print 'm:', m
        print 'n:', n
        for i in m:
            a = 0
            for j, k in zip(i, n):
                a = a + j * k
            mul.append(a)
        return mul

    def getCoefficient(self, A, B):
        A_inverse = self.getMatrixInverse(A)
        C = self.getMatrixMultiplication(A_inverse, B)
        # print('*************')
        # print(A_inverse)
        ##print(B)
        # print(C)
        # print('*************')
        return C

    def getYCap(self, coefficient, Xin):
        Ycap = coefficient[len(coefficient) - 1]
        for index in range(1, len(coefficient)):
            # print(index, Ycap)
            Ycap = Ycap + coefficient[index] * pow(Xin, index)

        return Ycap

    def getTranspose(self, A, M, N):
        """
        A = [[1,2],[3,4],[5,6]]
        :param A:
        :return:
        """
        B = [[0 for x in range(M)] for y in range(N)]
        for i in range(N):
            for j in range(M):
                B[i][j] = A[j][i]
        return B

    def getMultiplication(self, X, Y):
        return [[sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]