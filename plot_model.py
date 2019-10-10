from config import *
from nonlinear_regression2 import gauss_newton_method
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

"""
from sympy import symbols
from sympy.plotting import plot
x = symbols('x')
c = gauss_newton_method(init_coeff, init_cnt, expr, symbol_list)
print c
y = c[0]*(1.0 - exp(-c[1]*x))
print y
plot(y, (x, -100, 100))
"""
#print(Ycap)
#"""
#plt.axis([-50, 100, -50, 100])

x_axis = np.linspace(-5,5,100)

print len(x_axis)
print x_axis
print type(x_axis)
c = gauss_newton_method(init_coeff, init_cnt, expr, symbol_list)
#y = x**(size-4)*coefficient[size-4]+x**(size-3)*coefficient[size-3]+x**(size-2)*coefficient[size-2]+x**(size-1)*coefficient[size-1]
y_axis = np.empty(x_axis.shape)

for i in range(len(x_axis)):
    y_axis[i] = (c[0]*(1.0-exp(-c[1]*x))).subs({x:x_axis[i]}).evalf()

print y_axis
print type(y_axis)
plt.plot(x_axis, y_axis, '-r', label='a0*(1-e^(-a1*X))')
plt.title('Graph of y=a0*(1-e^(-a1*X))')
plt.xlabel('x', color='#1C2833')
plt.ylabel('y', color='#1C2833')
plt.legend(loc='upper left')
plt.grid()
plt.show()#"""