class LinearRegression:

    @staticmethod
    def get_cofactor(arr, temp, p, q, n):
        i = 0
        j = 0

        for row in range(n):
            for col in range(n):
                if row != p and col != q:
                    temp[i][j] = arr[row][col]
                    j += 1

                    if j == n-1:
                        j = 0
                        i += 1

    def get_det(self, arr, n):
        D = 0

        if n == 1:
            return arr[0][0]

        temp = []
        for i in range(N):
            temp.append([])
            for j in range(N):
                temp[i].append([])

        sign = 1

        for f in range(n):
            self.get_cofactor(arr, temp, 0, f, n)
            D += sign * arr[0][f] * self.get_det(temp, n-1)
            sign = -sign

        return D

    def get_adjoint(self, arr, adj):
        if N == 1:
            adj[0][0] = 1
            return

        temp = []
        for i in range(N):
            temp.append([])
            for j in range(N):
                temp[i].append([])

        for i in range(N):
            for j in range(N):
                self.get_cofactor(arr, temp, i, j, N)

                sign = 1 if ((i + j) % 2 == 0) else -1

                # adj[p][q] = sign * get_matrix_determinant(tmp)
                adj[j][i] = sign * self.get_det(temp, N-1)

    def get_matrix_inverse(self, arr, inverse):
        # determinant = get_matrix_determinant(m)

        determinant = self.get_det(arr, N)
        # special case for 2x2 matrix:
        # if len(arr) == 2:
        #    return [[arr[1][1]/determinant, -1*arr[0][1]/determinant],
        #            [-1*arr[1][0]/determinant, arr[0][0]/determinant]]
        # find matrix of co-factors

        adj = []
        for i in range(N):
            adj.append([])
            for j in range(N):
                adj[i].append([])

        self.get_adjoint(arr, adj)

        for i in range(N):
            for j in range(N):
                inverse[i][j] = adj[i][j] / float(determinant)


linear = LinearRegression()

# x = '0, 1, 2, 3, 4'
# y = '1, 1.8, 3.3, 4.5, 6.3'
# y = '-4, -1, 4, 11, 20'

# x = '1, 2, 3, 4'
# y = '6, 11, 18, 27'

# x = '1, 2, 3, 4, 5, 6'
# y = '1200, 900, 600, 200, 110, 50'

# x = '71, 68, 73, 69, 67, 65, 66, 67'
# y = '69, 72, 70, 70, 68, 67, 68, 64'

# x = '-1, 0, 1, 2'
# y = '2, 5, 3, 0'

# x = '1, 2, 3, 4, 5, 6, 7, 8, 9'
# y = '2, 6, 7, 8, 10, 11, 11, 10, 9'

# x = '1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937'
# y = '352, 356, 357, 358, 360, 361, 361, 360, 359'

# y = '1, 1.8, 1.3, 2.5, 6.3'

# x = '1, 2, 3, 4, 5, 6, 7, 8, 9, 10'
# y = '7.5, 44.31, 60.8, 148.97, 222.5, 262.64, 289.06, 451.53, 439.62, 698.88'

x = '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, ' \
    '31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, ' \
    '59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, ' \
    '87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, ' \
    '112, 113, 114, 115, 116, 117, 118, 119, 120 '
y = '7.50, 44.31, 60.80, 148.97, 225.50, 262.64, 289.06, 451.53, 439.62, 698.88, 748.24, 896.46, 1038.78, 1214.04, '\
    '1377.08, 1579.86, 1763.14, 1993.92, 2196.96, 2456.22, 2678.54, 2966.76, 3207.88, 3525.54, 3784.98, 4132.56, ' \
    '4409.84, 4787.82, 5082.46, 5491.32, 5802.84, 6243.06, 6570.98, 7043.04, 7386.88, 7891.26, 8250.54, 8787.72, ' \
    '9161.96, 9732.42, 10121.14, 10725.36, 11128.08, 11766.54, 12182.78, 12855.96, 13285.24, 13993.62, 14435.46, ' \
    '15179.52, 15633.44, 16413.66, 16879.18, 17696.04, 18172.68, 19026.66, 19513.94 ,20405.52, 20902.96, 21832.62, ' \
    '22339.74, 23307.96, 23824.28, 24831.54, 25356.58, 26403.36, 26936.64, 28023.42, 28564.46, 29691.72, 30240.04, ' \
    '31408.26, 31963.38, 33173.04, 33734.48, 34986.06, 35553.34, 36847.32, 37419.96, 38756.82, 39334.34, 40714.56, ' \
    '41296.48, 42720.54, 43306.38, 44774.76, 45364.04, 46877.22, 47469.46, 49027.92, 49622.64, 51226.86, 51823.58, ' \
    '53474.04, 54072.28, 55769.46, 56368.74, 58113.12, 58712.96, 60505.02, 61104.94, 62945.16, 63544.68, 65433.54, ' \
    '66032.18, 67970.16, 68567.44, 70555.02, 71150.46, 73188.12, 73781.24, 75869.46, 76459.78, 78599.04, 79186.08, ' \
    '81376.86, 81960.14, 84202.92, 84781.96, 87077.22 '
degree_of_x: int = 2

independentInputArray = x.split(',')
dependentInputArray = y.split(',')

sigma_X = []
sigma_XY = []

x_count = 1
while x_count <= degree_of_x * 2:
    temp = 0
    for x in independentInputArray:
        temp = temp + pow(float(x), x_count)

    sigma_X.append(temp)
    x_count += 1

y_count = 0
while y_count <= degree_of_x:
    temp = 0
    number_of_x = 0
    for y in dependentInputArray:
        temp = temp + float(y) * (pow(float(independentInputArray[number_of_x]), y_count))
        number_of_x = number_of_x + 1

    sigma_XY.append(temp)
    y_count += 1

arr = []

sigma_X.insert(0, float(len(independentInputArray)))

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

linear.get_adjoint(arr, adj)
print('\n Array Adjoint \n')
for adjoint in adj:
    print(adjoint)
print('\n')

linear.get_matrix_inverse(arr, inverse)

print('\n Inverse of Array after finding x and y values \n')
for inv in inverse:
    print(inv)
print('\n')

result = []
for i in range(N):
    result.append([])
    for j in range(1):
        result[i].append(0)

for i in range(len(inverse)):
    for j in range(len(sigma_XY_Transpose[0])):
        for k in range(len(sigma_XY_Transpose)):
            result[i][j] += inverse[i][k] * sigma_XY_Transpose[k][j]

variable_count = 0
for res in result:
    print('printing \u03B2', variable_count, ' = ', res)
    variable_count += 1
