# How to use..?
# 1. import anova
# 2. anova_dictionary = anova.main(x_values_list, y_values_list, coefficients_array)
# NOTE: coefficients_array should be in the order of beta0, beta1, beta2 ...
# For example equation = 11x - 20
# coefficients_array = [-20, 11], x_values_list = (2, 4, 6, 8, 10), y_values_list = (6, 18, 38, 66, 102)

import scipy.stats as stats

# Structure of the dictionary we deal with
# This same dictionary will be returned with updated values once the computations are done successfully
anova = {
    'x': (),
    'y': (),
    'coefficients': [],
    'degrees_of_freedom': None,
    'y_bar': None,
    'y_cap': [],
    'y_cap_sum': None,
    'ssr': None,
    'sse': None,
    'msr': None,
    'mse': None,
    'f': None,
    'p': None,
    'confidence': None
}


def cal_average():
    """Calculates average (mean) of variable X"""
    anova['y_bar'] = sum(anova.get('y'))/len(anova.get('y'))


def cal_y_cap():
    """Calculates y_cap for given value of x"""
    coefficients = anova['coefficients']
    y_cap_list = []
    x_list = anova.get('x')
    for x in x_list:
        intermediate_sum = 0
        for index in range(len(coefficients)):
            if index == 0:
                intermediate_sum += coefficients[index]
            else:
                intermediate_sum += ((x ** index) * coefficients[index])

        y_cap_list.append(intermediate_sum)
    anova['y_cap'] = y_cap_list
    anova['y_cap_sum'] = sum(y_cap_list)


def cal_ssr():
    """Calculates SSR"""
    y_cap_list = anova.get('y_cap')
    ssr_sum = 0
    y_bar = anova['y_bar']
    for y in y_cap_list:
        ssr_sum = ssr_sum + ((y-y_bar)**2)
    anova['ssr'] = ssr_sum


def cal_sse():
    """Calculates SSE"""
    y_list = anova.get('y')
    y_cap_list = anova.get('y_cap')
    sse_sum = 0
    for y, y_cap in zip(y_list, y_cap_list):
        sse_sum = sse_sum + (y-y_cap)**2
    anova['sse'] = sse_sum


def cal_msr():
    """Calculates MSR with known SSR"""
    degrees_of_freedom = anova['degrees_of_freedom']
    anova['msr'] = anova['ssr']/(degrees_of_freedom-1)


def cal_mse():
    """Calculates MSE with known SSE"""
    degrees_of_freedom = anova['degrees_of_freedom']
    anova['mse'] = anova['sse']/(len(anova.get('y'))-degrees_of_freedom)


def cal_f_and_p():
    """Calculates F and determines P"""
    degrees_of_freedom = anova['degrees_of_freedom']
    f = anova['msr']/anova['mse']
    anova['f'] = f
    p = stats.f.sf(f, (degrees_of_freedom-1), (len(anova.get('y'))-degrees_of_freedom))
    anova['p'] = p
    anova['confidence'] = (1 - p) * 100


def main(x, y, coefficients):
    # Update the starter dictionary with actual data to start with
    anova['x'] = x
    anova['y'] = y
    anova['coefficients'] = coefficients
    # The coefficients are reversed here in order to get it in the right form
    # Actual line : anova['coefficients'] = coefficients
    anova['degrees_of_freedom'] = 2
    # Should update if its multi-variate

    cal_average()
    cal_y_cap()
    cal_ssr()
    cal_sse()
    cal_msr()
    cal_mse()
    cal_f_and_p()

    return anova


if __name__ == "__main__":
    main()
