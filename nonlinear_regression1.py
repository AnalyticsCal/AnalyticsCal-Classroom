from data import formA, formB, prettyPrint
from linear_algebra import getCoefficient, getYCap
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np
size = 4
A = formA()
print('A:', A)
#prettyPrint(A)
B = formB()
print('B:', B)

coefficient = getCoefficient(A, B)
#Ycap = getYCap(coefficient, Xin)
print('coefficient::', coefficient)
coefficient = coefficient[::-1]
print('coefficient::', coefficient)

#print(Ycap)
x = np.linspace(-5,5,100)
print 'x', x
y = x**(size-4)*coefficient[size-4]+x**(size-3)*coefficient[size-3]+x**(size-2)*coefficient[size-2]+x**(size-1)*coefficient[size-1]
print 'Y', y
plt.plot(x, y, '-r', label='y=B0+x^1*B1+x^2*B2+x^3*B3+B4*x^4')
plt.title('Graph of y=B0+x^1*B1+x^2*B2+x^3*B3+B4*x^4')
plt.xlabel('x', color='#1C2833')
plt.ylabel('y', color='#1C2833')
plt.legend(loc='upper left')
plt.grid()
plt.show()