def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant


def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors


def getMatrixMultiplication(m,n):
    mul = []
    print 'm:', m
    print 'n:', n
    for i in m:
        a = 0
        for j,k in zip(i,n):
            a = a + j*k
        mul.append(a)
    return mul


def getCoefficient(A, B):
    A_inverse = getMatrixInverse(A)
    C = getMatrixMultiplication(A_inverse, B)
    #print('*************')
    #print(A_inverse)
    ##print(B)
    #print(C)
    #print('*************')
    return C

def getYCap(coefficient, Xin):
    Ycap = coefficient[len(coefficient)-1]
    for index in range(1, len(coefficient)):
        #print(index, Ycap)
        Ycap = Ycap + coefficient[index]*pow(Xin, index)

    return Ycap


def getTranspose(A, M, N):
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

def getMultiplication(X,Y):
    return [[sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]