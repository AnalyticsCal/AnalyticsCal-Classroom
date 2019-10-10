from sympy import *

order = 2
symbol_list = []
init_coeff = []
for i in range(order):
    symbol_list.append(symbols('m{}'.format(i), real=True))
    init_coeff.append(1.0)

x = symbols('x', real=True)
expr = symbol_list[0]*(1.0-exp(-symbol_list[1]*x))
iteration_cnt = 20
init_cnt = 0